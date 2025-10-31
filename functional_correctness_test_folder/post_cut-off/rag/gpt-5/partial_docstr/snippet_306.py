from typing import Any
import re
import difflib
from copy import deepcopy


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''
    BODY_PREFIX = '$response.body#'
    HEADERS_PREFIX = '$response.headers#'

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
        # Work on a copy to avoid side-effects
        wf = workflow

        def traverse(node: Any) -> None:
            if isinstance(node, dict):
                # Treat any dict with "outputs" as a potential step
                if 'outputs' in node and isinstance(node['outputs'], dict):
                    endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                        node, endpoints)
                    if endpoint_data:
                        schema, headers = OutputMappingValidator._extract_response_info(
                            endpoint_data)
                        fixed = OutputMappingValidator._validate_step_outputs(
                            node['outputs'], schema or {}, headers or {})
                        node['outputs'] = fixed
                # Recurse into children
                for v in node.values():
                    traverse(v)
            elif isinstance(node, list):
                for item in node:
                    traverse(item)

        traverse(wf)
        return wf

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        '''Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        '''
        # Possible locations for operationId or method/path info
        op_id = step.get('operationId')
        req = step.get('request') if isinstance(
            step.get('request'), dict) else {}
        op_id = op_id or req.get('operationId') or req.get(
            'operation_id') or step.get('opId') or step.get('id')
        method = (req.get('method') or step.get('method') or '').lower()
        path = req.get('path') or step.get(
            'path') or req.get('url') or step.get('url')

        # Strong match by key
        if op_id and op_id in endpoints:
            return endpoints[op_id]

        # Try match by stored operationId field
        if op_id:
            for data in endpoints.values():
                if isinstance(data, dict) and data.get('operationId') == op_id:
                    return data

        # Try match by "METHOD path" key
        if method and path:
            combo_key = f'{method.upper()} {path}'
            if combo_key in endpoints:
                return endpoints[combo_key]
            # Search values for method+path
            for data in endpoints.values():
                if not isinstance(data, dict):
                    continue
                d_method = (data.get('method') or data.get(
                    'http_method') or '').lower()
                d_path = data.get('path') or data.get(
                    'route') or data.get('url')
                if d_method == method and d_path == path:
                    return data

        # As a fallback, if there's only one endpoint, use it
        if len(endpoints) == 1:
            return next(iter(endpoints.values()))

        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        # Normalize potential locations
        responses = (
            endpoint_data.get('responses')
            or endpoint_data.get('response')
            or endpoint_data.get('operation', {}).get('responses')
            or {}
        )

        # Choose a preferred response: prioritize 2xx, then default, then first available
        def pick_response_key(resp_dict: dict[str, Any]) -> str | None:
            if not resp_dict:
                return None
            # exact 200 first, then other 2xx
            if '200' in resp_dict:
                return '200'
            twoxx = [k for k in resp_dict.keys(
            ) if re.fullmatch(r'2\d\d', str(k))]
            if twoxx:
                return sorted(twoxx)[0]
            if 'default' in resp_dict:
                return 'default'
            # otherwise first key
            return next(iter(resp_dict.keys()), None)

        key = pick_response_key(responses) if isinstance(
            responses, dict) else None
        response_obj = responses.get(key, {}) if key else {}

        # Headers
        headers = response_obj.get(
            'headers') or endpoint_data.get('headers') or {}

        # Schema
        schema: dict[str, Any] = {}

        # Some parsers may expose schema directly
        if 'schema' in response_obj and isinstance(response_obj['schema'], dict):
            schema = response_obj['schema']
        else:
            # OpenAPI v3 content-based
            content = response_obj.get('content', {})
            if isinstance(content, dict) and content:
                if 'application/json' in content:
                    media = content['application/json']
                else:
                    # pick first media type
                    media = next(iter(content.values()), {})
                schema = media.get('schema', {}) if isinstance(
                    media, dict) else {}
        # Fallbacks at top-level
        if not schema:
            schema = endpoint_data.get(
                'response_schema') or endpoint_data.get('schema') or {}

        # Ensure dicts
        schema = schema if isinstance(schema, dict) else {}
        headers = headers if isinstance(headers, dict) else {}

        return schema, headers

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
        if not isinstance(outputs, dict):
            return outputs

        fixed: dict[str, str] = {}

        # Build candidates from schema (body) and headers
        flat_schema = OutputMappingValidator._flatten_schema(schema)
        # Map header names (case-insensitive) to canonical mapping strings
        header_candidates: dict[str, str] = {}
        for h_name in headers.keys():
            if isinstance(h_name, str):
                header_candidates[h_name.lower(
                )] = f'{OutputMappingValidator.HEADERS_PREFIX}/{h_name}'

        # Precompute normalized body paths
        normalized_body_paths = {}
        for _, body_path in flat_schema.items():
            norm = OutputMappingValidator._normalize_property_path(body_path)
            normalized_body_paths[norm] = body_path

        for out_name, mapping in outputs.items():
            if not isinstance(mapping, str):
                # Try to infer mapping
                best_body = OutputMappingValidator._find_best_property_match(
                    str(out_name), flat_schema)
                if best_body:
                    fixed[out_name] = best_body
                    continue
                best_header_key = OutputMappingValidator._find_best_match(
                    str(out_name).lower(), list(header_candidates.keys()))
                if best_header_key:
                    fixed[out_name] = header_candidates[best_header_key]
                    continue
                fixed[out_name] = mapping
                continue

            m = mapping.strip()

            # If header mapping
            if m.startswith(OutputMappingValidator.HEADERS_PREFIX):
                # Extract header name
                header_name = m[len(OutputMappingValidator.HEADERS_PREFIX):].lstrip(
                    '/').strip()
                if header_name:
                    # Validate presence (case-insensitive)
                    lookup = header_candidates.get(header_name.lower())
                    if lookup:
                        fixed[out_name] = lookup
                        continue
                # Try to correct by best match using output name or provided header segment
                candidate_target = header_name or str(out_name)
                best = OutputMappingValidator._find_best_match(
                    candidate_target.lower(), list(header_candidates.keys()))
                if best:
                    fixed[out_name] = header_candidates[best]
                    continue
                # Fallback: try body
                best_body = OutputMappingValidator._find_best_property_match(
                    str(out_name), flat_schema)
                if best_body:
                    fixed[out_name] = best_body
                else:
                    fixed[out_name] = m
                continue

            # If body mapping
            if m.startswith(OutputMappingValidator.BODY_PREFIX):
                norm = OutputMappingValidator._normalize_property_path(m)
                if norm in normalized_body_paths:
                    # Valid mapping
                    fixed[out_name] = normalized_body_paths[norm]
                    continue
                # Try correcting using output name
                best_body = OutputMappingValidator._find_best_property_match(
                    str(out_name), flat_schema)
                if best_body:
                    fixed[out_name] = best_body
                    continue
                # Try correcting using last path segment from provided mapping
                last_seg = ''
                try:
                    last_seg = m.split('#', 1)[1].strip('/').split('/')[-1]
                except Exception:
                    last_seg = ''
                if last_seg:
                    best_alt_key = OutputMappingValidator._find_best_match(
                        last_seg.lower(), list(flat_schema.keys()))
                    if best_alt_key:
                        fixed[out_name] = flat_schema[best_alt_key]
                        continue
                # Fallback as-is
                fixed[out_name] = m
                continue

            # If mapping is neither body nor headers, infer best location
            best_body = OutputMappingValidator._find_best_property_match(
                str(out_name), flat_schema)
            if best_body:
                fixed[out_name] = best_body
                continue
            best_header_key = OutputMappingValidator._find_best_match(
                str(out_name).lower(), list(header_candidates.keys()))
            if best_header_key:
                fixed[out_name] = header_candidates[best_header_key]
                continue
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
            return path  # type: ignore[return-value]

        s = path.strip()
        # Separate prefix if present (e.g., "$response.body#")
        prefix = ''
        frag = s
        if '#' in s:
            prefix, _, frag = s.partition('#')
        frag = frag.lstrip('#')

        # Remove JSON Pointer array indices: '/0', '/1', etc.
        # Only remove segments that are purely numeric.
        segments = [seg for seg in frag.split('/') if seg != '']
        segments = [seg for seg in segments if not seg.isdigit()]

        normalized_frag = '/' + '/'.join(segments) if segments else ''
        if prefix:
            # Ensure prefix keeps trailing '#'
            prefix = prefix.rstrip()
            if not prefix.endswith('#'):
                prefix = prefix + '#'
            return f'{prefix}{normalized_frag}'
        return normalized_frag

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

        def normalize(s: str) -> str:
            return re.sub(r'[^a-z0-9]', '', s.lower())

        t = normalize(target)
        best = None
        best_score = 0.0
        for c in candidates:
            score = difflib.SequenceMatcher(a=t, b=normalize(c)).ratio()
            if score > best_score:
                best_score = score
                best = c
        # Require a minimal similarity to avoid random matches
        if best is not None and best_score >= 0.5:
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
        best_key = OutputMappingValidator._find_best_match(
            str(output_name), list(flat_schema.keys()))
        return flat_schema.get(best_key) if best_key else None

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.
        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.
        Returns:
            A dictionary mapping property names to their paths.
        '''
        result: dict[str, str] = {}

        def add_candidates(path_segments: list[str]) -> None:
            if not path_segments:
                return
            # Build forms: leaf name, dot path, slash path
            filtered = [
                seg for seg in path_segments if seg and not seg.isdigit()]
            if not filtered:
                return
            leaf = filtered[-1]
            dot_path = '.'.join(filtered)
            slash_path = '/'.join(filtered)
            mapping_value = f'{OutputMappingValidator.BODY_PREFIX}/{slash_path}'

            # Candidate keys (case-insensitive stored)
            for key in {leaf, dot_path, slash_path}:
                k = key.lower()
                if k and k not in result:
                    result[k] = mapping_value

        def walk(schema: dict[str, Any], path_segments: list[str]) -> None:
            if not isinstance(schema, dict):
                add_candidates(path_segments)
                return

            # Handle composition keywords: allOf/oneOf/anyOf
            for comp in ('allOf', 'oneOf', 'anyOf'):
                if comp in schema and isinstance(schema[comp], list):
                    for sub in schema[comp]:
                        walk(sub if isinstance(sub, dict)
                             else {}, path_segments)

            t = schema.get('type')
            # If no explicit type, attempt to infer
            if not t:
                if 'properties' in schema:
                    t = 'object'
                elif 'items' in schema:
                    t = 'array'

            if t == 'object' or 'properties' in schema:
                props = schema.get('properties', {})
                if isinstance(props, dict):
                    for name, subschema in props.items():
                        if isinstance(name, str):
                            new_path = path_segments + [name]
                            add_candidates(new_path)
                            walk(subschema if isinstance(
                                subschema, dict) else {}, new_path)
                else:
                    add_candidates(path_segments)
            elif t == 'array':
                items = schema.get('items', {})
                # Represent array index with a numeric segment that will be normalized out
                walk(items if isinstance(items, dict)
                     else {}, path_segments + ['0'])
            else:
                # Primitive leaf
                add_candidates(path_segments)

        # Detect if provided dict is full schema or already properties
        if 'properties' in properties or 'type' in properties or 'items' in properties:
            walk(properties, [seg for seg in prefix.split(
                '.') if seg] if prefix else [])
        else:
            # Treat as properties dict
            base_path = [seg for seg in prefix.split(
                '.') if seg] if prefix else []
            for name, subschema in (properties or {}).items():
                if isinstance(name, str):
                    new_path = base_path + [name]
                    add_candidates(new_path)
                    walk(subschema if isinstance(
                        subschema, dict) else {}, new_path)

        return result
