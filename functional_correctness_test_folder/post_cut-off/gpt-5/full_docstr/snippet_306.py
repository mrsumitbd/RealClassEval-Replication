from __future__ import annotations
from typing import Any
import re
import difflib


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        '''Validate and fix output mappings in a workflow.
        This function checks all output mappings in a workflow against the
        corresponding response schemas from the OpenAPI spec and fixes any
        inconsistencies.
        Args:
            workflow: The workflow to validate.
            openapi_spec: The OpenAPI specification.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The validated and fixed workflow.
        '''
        steps = workflow.get('steps', [])
        if not isinstance(steps, list):
            return workflow

        for step in steps:
            outputs = step.get('outputs')
            if not isinstance(outputs, dict):
                continue

            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue

            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            fixed_outputs = OutputMappingValidator._validate_step_outputs(
                outputs, schema, headers)
            step['outputs'] = fixed_outputs

        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        '''Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        '''
        if not isinstance(endpoints, dict):
            return None

        # Common identifiers to look for
        op_id = step.get('operationId') or step.get(
            'operation_id') or step.get('operation') or step.get('endpointId')
        if isinstance(op_id, dict):
            op_id = op_id.get('operationId') or op_id.get('operation_id')
        if isinstance(op_id, str) and op_id in endpoints:
            return endpoints.get(op_id)

        # Some parsers store path+method
        path = step.get('path') or step.get('url') or step.get('endpoint')
        method = (step.get('method') or '').lower()
        if path and method:
            # Attempt direct key match like "GET /pets"
            key_variants = [
                f'{method.upper()} {path}',
                f'{method.lower()} {path}',
                f'{path} {method.lower()}',
                f'{path} {method.upper()}',
                f'{path}::{method.lower()}',
                f'{method.lower()}::{path}',
            ]
            for k in key_variants:
                if k in endpoints:
                    return endpoints[k]

        # Fallback: search by operationId property inside endpoint data
        if isinstance(op_id, str):
            for data in endpoints.values():
                if isinstance(data, dict) and data.get('operationId') == op_id:
                    return data

        # Last resort: fuzzy match by operationId string across keys
        if isinstance(op_id, str):
            best_key = OutputMappingValidator._find_best_match(
                op_id, list(endpoints.keys()) or [])
            if best_key:
                return endpoints.get(best_key)

        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        responses = endpoint_data.get('responses') if isinstance(
            endpoint_data, dict) else None
        if not isinstance(responses, dict):
            return {}, {}

        # Prefer 2xx responses
        preferred_codes = ['200', '201', '202', '204']
        selected = None
        for code in preferred_codes:
            if code in responses:
                selected = responses[code]
                break
        if not selected:
            # pick the first defined response
            selected = next(iter(responses.values())) if responses else None
        if not isinstance(selected, dict):
            return {}, {}

        headers = selected.get('headers') if isinstance(
            selected.get('headers'), dict) else {}

        # Find the JSON schema if present
        schema: dict[str, Any] = {}
        content = selected.get('content') if isinstance(
            selected.get('content'), dict) else {}
        if isinstance(content, dict):
            # Prefer JSON content types
            json_cts = [ct for ct in content.keys() if 'json' in ct.lower()]
            ct = json_cts[0] if json_cts else (
                next(iter(content.keys()), None))
            if ct:
                media = content.get(ct) or {}
                if isinstance(media, dict):
                    sch = media.get('schema')
                    if isinstance(sch, dict):
                        schema = sch

        # In case of direct schema under response (less common)
        if not schema and isinstance(selected.get('schema'), dict):
            schema = selected['schema']

        return schema or {}, headers or {}

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        '''Validate and fix output mappings for a step.
        Args:
            outputs: The output mappings to validate.
            schema: The response schema.
            headers: The response headers.
        Returns:
            The validated and fixed output mappings.
        '''
        fixed: dict[str, str] = {}

        # Prepare flattened schema of body properties
        properties = {}
        if isinstance(schema, dict):
            # Resolve object schemas to their properties
            if 'properties' in schema and isinstance(schema['properties'], dict):
                properties = schema['properties']
            elif schema.get('type') == 'array' and isinstance(schema.get('items'), dict):
                items = schema['items']
                if isinstance(items, dict) and 'properties' in items and isinstance(items['properties'], dict):
                    properties = items['properties']
            # For allOf/oneOf/anyOf, merge basic properties if present
            for combiner in ('allOf', 'oneOf', 'anyOf'):
                if combiner in schema and isinstance(schema[combiner], list):
                    for s in schema[combiner]:
                        if isinstance(s, dict) and isinstance(s.get('properties'), dict):
                            properties = {**properties, **s['properties']}
        flat_schema = OutputMappingValidator._flatten_schema(properties)

        # Prepare headers list with canonical casing
        header_names = []
        header_name_map = {}  # lowercase -> canonical
        if isinstance(headers, dict):
            for k in headers.keys():
                if isinstance(k, str):
                    header_names.append(k)
                    header_name_map[k.lower()] = k

        for out_name, mapping in outputs.items():
            # Default: if mapping is not a string, attempt to infer
            if not isinstance(mapping, str) or not mapping.strip():
                best_body = OutputMappingValidator._find_best_property_match(
                    out_name, flat_schema)
                if best_body:
                    fixed[out_name] = f'$.body.{best_body}'
                else:
                    # Try header match if body not available
                    best_header = OutputMappingValidator._find_best_match(
                        out_name, [h.lower() for h in header_names])
                    if best_header:
                        canonical = header_name_map.get(
                            best_header.lower(), best_header)
                        fixed[out_name] = f'$.headers.{canonical}'
                    else:
                        fixed[out_name] = mapping if isinstance(
                            mapping, str) else ''
                continue

            m = mapping.strip()

            # Determine if mapping points to headers or body
            lower_m = m.lower()
            if '.headers.' in lower_m or lower_m.startswith('headers.'):
                # Extract header name
                # Accept patterns: "$.headers.X", "headers.X"
                parts = re.split(r'\$?\.\s*headers\.', m, flags=re.IGNORECASE)
                header = parts[-1] if parts else ''
                header = header.strip()
                if not header:
                    # Try infer best header
                    best_header = OutputMappingValidator._find_best_match(
                        out_name, [h.lower() for h in header_names])
                    if best_header:
                        canonical = header_name_map.get(
                            best_header.lower(), best_header)
                        fixed[out_name] = f'$.headers.{canonical}'
                    else:
                        fixed[out_name] = m
                else:
                    canonical = header_name_map.get(header.lower())
                    if canonical:
                        fixed[out_name] = f'$.headers.{canonical}'
                    else:
                        # Header not found -> try best match
                        best_header = OutputMappingValidator._find_best_match(
                            header.lower(), [h.lower() for h in header_names])
                        if best_header:
                            canonical = header_name_map.get(
                                best_header.lower(), best_header)
                            fixed[out_name] = f'$.headers.{canonical}'
                        else:
                            fixed[out_name] = m
                continue

            # Treat as body mapping
            # Extract path after "$.body." or "body." or "$." or starting directly
            body_path = m
            for pat in [r'^\$\.\s*body\.', r'^body\.', r'^\$\.\s*', r'^\$\[']:
                body_path = re.sub(pat, '', body_path, flags=re.IGNORECASE)
            body_path = body_path.strip().lstrip('.')

            # Normalize indices and compare to flattened schema
            normalized = OutputMappingValidator._normalize_property_path(
                body_path)

            # Direct match
            if normalized in flat_schema:
                fixed[out_name] = f'$.body.{normalized}'
                continue

            # Try last-segment based matching if mapping was different
            # Attempt to find best property based on output name first
            best_prop = OutputMappingValidator._find_best_property_match(
                out_name, flat_schema)
            if best_prop:
                fixed[out_name] = f'$.body.{best_prop}'
                continue

            # Try matching based on provided path token
            last_token = normalized.split(
                '.')[-1] if normalized else normalized
            if last_token:
                candidates = list(flat_schema.keys())
                best = OutputMappingValidator._find_best_match(
                    last_token, [c.split('.')[-1] for c in candidates])
                if best:
                    # Map back to full path with that last token (choose first)
                    for full in candidates:
                        if full.split('.')[-1].lower() == best.lower():
                            fixed[out_name] = f'$.body.{full}'
                            break
                    else:
                        fixed[out_name] = m
                    continue

            # No good match found; keep original mapping
            fixed[out_name] = m

        return fixed

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        '''Normalize a property path by removing array indices.
        Args:
            path: The property path to normalize.
        Returns:
            The normalized property path.
        '''
        if not isinstance(path, str):
            return ''
        p = path.strip().lstrip('.')
        # Replace [number] with []
        p = re.sub(r'\[\s*\d+\s*\]', '[]', p)
        # Replace consecutive dots
        p = re.sub(r'\.+', '.', p)
        return p

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates:
            return None
        if not isinstance(target, str):
            return None
        target_norm = target.strip().lower().replace('_', '').replace('-', '')
        cand_map = {c: (c.strip().lower().replace('_', '').replace(
            '-', '') if isinstance(c, str) else '') for c in candidates}
        best = None
        best_ratio = 0.0
        for orig, cand in cand_map.items():
            if not cand:
                continue
            ratio = difflib.SequenceMatcher(a=target_norm, b=cand).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best = orig
        # Require a minimal similarity threshold
        if best is not None and best_ratio >= 0.6:
            return best
        return None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        '''Find the best matching property in the schema for an output name.
        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.
        Returns:
            The path to the matching property, or None if no match is found.
        '''
        if not flat_schema:
            return None
        if not isinstance(output_name, str):
            return None

        # Try exact and case-insensitive matches on last segments
        last_segments = {path.split(
            '.')[-1]: path for path in flat_schema.keys()}
        if output_name in last_segments:
            return last_segments[output_name]
        for k, v in last_segments.items():
            if k.lower() == output_name.lower():
                return v

        # Normalize output name (remove suffixes like _id vs id)
        normalized_name = output_name.strip().lower().replace('_', '').replace('-', '')

        # Try fuzzy match against last segments
        best_last = OutputMappingValidator._find_best_match(normalized_name, [k.replace(
            '_', '').replace('-', '').lower() for k in last_segments.keys()])
        if best_last:
            # Map back to original path by finding the segment case-insensitively
            for seg, path in last_segments.items():
                if seg.replace('_', '').replace('-', '').lower() == best_last:
                    return path

        # Try fuzzy match against full paths
        best_full = OutputMappingValidator._find_best_match(
            normalized_name, [p.replace('.', '') for p in flat_schema.keys()])
        if best_full:
            # Pick the first path whose stripped version matches the best_full
            for p in flat_schema.keys():
                if p.replace('.', '') == best_full:
                    return p

        return None

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.
        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.
        Returns:
            A dictionary mapping property names to their paths.
        '''
        flat: dict[str, str] = {}
        if not isinstance(properties, dict):
            return flat

        def add_path(path: str, typ: str | None = None):
            key = path.lstrip('.')
            flat[key] = typ or 'any'

        for prop_name, prop_schema in properties.items():
            current_path = f'{prefix}.{prop_name}' if prefix else prop_name
            if not isinstance(prop_schema, dict):
                add_path(current_path, 'any')
                continue

            typ = prop_schema.get('type')
            if typ == 'object':
                nested_props = prop_schema.get('properties')
                if isinstance(nested_props, dict) and nested_props:
                    # include the object itself and its nested properties
                    add_path(current_path, 'object')
                    nested_flat = OutputMappingValidator._flatten_schema(
                        nested_props, current_path)
                    flat.update(nested_flat)
                else:
                    add_path(current_path, 'object')
            elif typ == 'array':
                items = prop_schema.get('items') if isinstance(
                    prop_schema.get('items'), dict) else {}
                array_path = f'{current_path}[]'
                add_path(array_path, 'array')
                if isinstance(items, dict):
                    if items.get('type') == 'object' and isinstance(items.get('properties'), dict):
                        # Flatten properties within array items
                        nested_flat = OutputMappingValidator._flatten_schema(
                            items.get('properties', {}), array_path)
                        flat.update(nested_flat)
                    elif items.get('type') == 'array':
                        # Nested arrays
                        add_path(f'{array_path}[]', 'array')
                    else:
                        # Primitive array items
                        add_path(array_path, items.get('type', 'any'))
            else:
                # Primitive or unknown type
                add_path(current_path, typ or 'any')

            # Handle composition keywords within properties
            for combiner in ('allOf', 'oneOf', 'anyOf'):
                if combiner in prop_schema and isinstance(prop_schema[combiner], list):
                    for s in prop_schema[combiner]:
                        if isinstance(s, dict):
                            if s.get('type') == 'object' and isinstance(s.get('properties'), dict):
                                nested_flat = OutputMappingValidator._flatten_schema(
                                    s['properties'], current_path)
                                flat.update(nested_flat)
                            elif 'properties' in s and isinstance(s['properties'], dict):
                                nested_flat = OutputMappingValidator._flatten_schema(
                                    s['properties'], current_path)
                                flat.update(nested_flat)

        return flat
