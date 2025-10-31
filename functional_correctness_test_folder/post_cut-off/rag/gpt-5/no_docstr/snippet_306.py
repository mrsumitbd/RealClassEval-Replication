from typing import Any
import copy
import difflib
import re


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
        wf = copy.deepcopy(workflow)
        steps = wf.get('steps') or wf.get('workflow', {}).get('steps') or []
        if not isinstance(steps, list):
            return wf

        for step in steps:
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue

            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)

            outputs_obj = step.get('outputs')
            if not outputs_obj:
                continue

            original_is_list = isinstance(outputs_obj, list)
            # Normalize to dict[str, str]
            if original_is_list:
                outputs_dict: dict[str, str] = {}
                for item in outputs_obj:
                    if isinstance(item, dict):
                        name = item.get('name') or item.get(
                            'key') or item.get('output')
                        value = item.get('value') or item.get(
                            'path') or item.get('mapping')
                        if isinstance(name, str) and name:
                            outputs_dict[name] = value if isinstance(
                                value, str) else ''
                if not outputs_dict:
                    continue
            elif isinstance(outputs_obj, dict):
                outputs_dict = {k: v for k,
                                v in outputs_obj.items() if isinstance(k, str)}
            else:
                continue

            fixed_outputs = OutputMappingValidator._validate_step_outputs(
                outputs_dict, schema or {}, headers or {})

            # Write back in the original structure
            if original_is_list:
                new_list = []
                for item in outputs_obj:
                    if isinstance(item, dict):
                        name = item.get('name') or item.get(
                            'key') or item.get('output')
                        if isinstance(name, str) and name in fixed_outputs:
                            # Preserve original key field and use 'value'
                            new_item = dict(item)
                            new_item['value'] = fixed_outputs[name]
                            new_list.append(new_item)
                        else:
                            new_list.append(item)
                    else:
                        new_list.append(item)
                step['outputs'] = new_list
            else:
                step['outputs'] = fixed_outputs

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
        # Try to resolve by operationId first
        op_id = (
            step.get('operationId')
            or step.get('operation_id')
            or (step.get('operation') or {}).get('operationId')
            or (step.get('request') or {}).get('operationId')
        )
        if isinstance(op_id, str) and op_id in endpoints:
            return endpoints[op_id]

        # Try to resolve by method + path
        method = (
            step.get('method')
            or (step.get('operation') or {}).get('method')
            or (step.get('request') or {}).get('method')
        )
        path = (
            step.get('path')
            or (step.get('operation') or {}).get('path')
            or (step.get('request') or {}).get('path')
            or (step.get('http') or {}).get('path')
        )

        method_l = method.lower() if isinstance(method, str) else None
        if method_l and isinstance(path, str):
            # Search endpoints dict values for match
            for data in endpoints.values():
                d_method = (data.get('method') or data.get(
                    'httpMethod') or '').lower()
                d_path = data.get('path') or data.get(
                    'route') or data.get('url')
                if d_method == method_l and isinstance(d_path, str) and d_path == path:
                    return data

        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        # Try common OpenAPI shapes
        responses = endpoint_data.get(
            'responses') or endpoint_data.get('response') or {}
        if not isinstance(responses, dict):
            return {}, {}

        # Prefer 2xx responses with priority 200 > 201 > others
        preferred_order = ['200', '201', '204']
        code = None
        for c in preferred_order:
            if c in responses:
                code = c
                break
        if not code:
            # Any 2xx
            for c in responses:
                if str(c).startswith('2'):
                    code = str(c)
                    break
        if not code:
            # Any response at all
            if responses:
                code = next(iter(responses.keys()))
            else:
                return {}, {}

        resp_obj = responses.get(code) or {}
        headers = resp_obj.get('headers') or {}
        schema: dict[str, Any] = {}

        # Handle content-based schema
        content = resp_obj.get('content')
        if isinstance(content, dict) and content:
            # Prefer JSON-like mimes
            json_mimes = ['application/json',
                          'application/*+json', 'text/json']
            mime = None
            for m in json_mimes:
                if m in content:
                    mime = m
                    break
            if not mime:
                # Fall back to first available
                mime = next(iter(content.keys()), None)
            if mime:
                schema = (content.get(mime) or {}).get('schema') or {}

        # Some descriptions place schema directly on response object
        if not schema and isinstance(resp_obj.get('schema'), dict):
            schema = resp_obj['schema']

        # Normalize headers to dict shape
        if not isinstance(headers, dict):
            headers = {}

        return schema if isinstance(schema, dict) else {}, headers

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
        # Flatten body schema
        properties = {}
        # Attempt to extract object properties robustly
        if isinstance(schema, dict):
            if 'properties' in schema and isinstance(schema['properties'], dict):
                properties = schema['properties']
            elif schema.get('type') == 'array' and isinstance(schema.get('items'), dict):
                items = schema['items']
                if isinstance(items.get('properties'), dict):
                    properties = items['properties']
            # Try allOf/oneOf/anyOf
            for combiner in ('allOf', 'oneOf', 'anyOf'):
                if combiner in schema and isinstance(schema[combiner], list):
                    for sub in schema[combiner]:
                        if isinstance(sub, dict) and isinstance(sub.get('properties'), dict):
                            properties.update(sub['properties'])

        flat_schema = OutputMappingValidator._flatten_schema(properties)

        header_names = list(headers.keys()) if isinstance(
            headers, dict) else []
        header_names_lower = {h.lower(): h for h in header_names}

        for out_name, path in outputs.items():
            value = path if isinstance(path, str) else ''
            val = value.strip()

            # If clearly a header mapping
            low = val.lower()
            if low.startswith('headers.') or low.startswith('header.'):
                header_key = val.split('.', 1)[1] if '.' in val else ''
                header_key = header_key.strip()
                header_key_l = header_key.lower()
                if header_key_l in header_names_lower:
                    fixed[out_name] = f'headers.{header_names_lower[header_key_l]}'
                    continue
                # Try best match for header
                best_header = OutputMappingValidator._find_best_match(
                    header_key, header_names)
                if best_header:
                    fixed[out_name] = f'headers.{best_header}'
                else:
                    fixed[out_name] = val or f'headers.{header_key}'
                continue

            # Treat as body mapping
            # Strip common prefixes
            stripped = val
            for pf in ('response.body.', 'response.data.', 'response.', 'body.', 'data.', '$.body.', '$.data.', '$.'):
                if stripped.lower().startswith(pf):
                    stripped = stripped[len(pf):]
                    break

            stripped = OutputMappingValidator._normalize_property_path(
                stripped)

            # If stripped path exactly matches any flattened path, accept
            if stripped and stripped in flat_schema.values():
                fixed[out_name] = f'body.{stripped}'
                continue

            # If path provided but not found, try to best-match against paths
            if stripped:
                best_path = OutputMappingValidator._find_best_match(
                    stripped, list(flat_schema.values()))
                if best_path:
                    fixed[out_name] = f'body.{best_path}'
                    continue

            # If we cannot use provided path, try to infer from output name
            best_from_name = OutputMappingValidator._find_best_property_match(
                out_name, flat_schema)
            if best_from_name:
                fixed[out_name] = f'body.{best_from_name}'
                continue

            # Last resort: keep original as-is or construct from name
            if val:
                fixed[out_name] = val
            else:
                # default to body.<name> if possible
                candidate = OutputMappingValidator._find_best_property_match(
                    out_name, flat_schema)
                fixed[out_name] = f'body.{candidate}' if candidate else out_name

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
        # Remove any template-like wrapping
        p = path.strip()
        # Remove array indices like [0], [*]
        p = re.sub(r'\[\s*\d+\s*\]', '', p)
        p = re.sub(r'\[\s*\*\s*\]', '', p)
        # Replace consecutive dots
        p = re.sub(r'\.+', '.', p)
        # Remove leading/trailing dots
        p = p.strip('.')
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
        if not candidates or not isinstance(target, str) or not target:
            return None

        def norm(s: str) -> str:
            s = s.lower()
            s = re.sub(r'[^a-z0-9]+', '', s)
            return s

        t = norm(target)
        if not t:
            return None

        best = None
        best_score = 0.0
        for c in candidates:
            if not isinstance(c, str):
                continue
            score = difflib.SequenceMatcher(None, t, norm(c)).ratio()
            if score > best_score:
                best = c
                best_score = score

        # Reasonable threshold to avoid wild mismatches
        if best is not None and best_score >= 0.6:
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
        if not isinstance(output_name, str) or not output_name:
            return None

        # Exact key match (case-insensitive)
        lower_keys = {k.lower(): k for k in flat_schema.keys()}
        if output_name.lower() in lower_keys:
            return flat_schema[lower_keys[output_name.lower()]]

        # Try removing separators and camel case variations
        candidates = list(flat_schema.keys())
        best_key = OutputMappingValidator._find_best_match(
            output_name, candidates)
        if best_key:
            return flat_schema.get(best_key)

        # As a fallback, try matching against last segment of paths
        path_last_segments = {path.split(
            '.')[-1]: path for path in flat_schema.values()}
        best_seg = OutputMappingValidator._find_best_match(
            output_name, list(path_last_segments.keys()))
        if best_seg:
            return path_last_segments[best_seg]

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

        def add_key(key: str, full_path: str) -> None:
            # Only add if not already present to keep the first occurrence
            if key not in flat:
                flat[key] = full_path

        def walk(props: dict[str, Any], pref: str = '') -> None:
            for name, meta in (props or {}).items():
                if not isinstance(name, str) or not isinstance(meta, dict):
                    continue
                current_path = f'{pref}.{name}' if pref else name
                add_key(name, current_path)

                # If object, recurse into properties
                if meta.get('type') == 'object' and isinstance(meta.get('properties'), dict):
                    walk(meta['properties'], current_path)

                # Handle arrays of objects
                if meta.get('type') == 'array':
                    items = meta.get('items')
                    if isinstance(items, dict) and items.get('type') == 'object' and isinstance(items.get('properties'), dict):
                        walk(items['properties'], current_path)

                # Combine properties from allOf/oneOf/anyOf
                for combiner in ('allOf', 'oneOf', 'anyOf'):
                    if combiner in meta and isinstance(meta[combiner], list):
                        for sub in meta[combiner]:
                            if isinstance(sub, dict) and isinstance(sub.get('properties'), dict):
                                walk(sub['properties'], current_path)

        if isinstance(properties, dict):
            walk(properties, prefix.strip('.'))

        return flat
