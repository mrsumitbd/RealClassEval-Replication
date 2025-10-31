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
        steps = workflow.get('steps') or workflow.get(
            'workflow', {}).get('steps') or []
        if not isinstance(steps, list):
            return workflow

        for step in steps:
            try:
                outputs = step.get('outputs')
                if not outputs or not isinstance(outputs, dict):
                    continue

                endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                    step, endpoints)
                if not endpoint_data:
                    continue

                schema, headers = OutputMappingValidator._extract_response_info(
                    endpoint_data)
                fixed = OutputMappingValidator._validate_step_outputs(
                    outputs, schema or {}, headers or {})
                if fixed is not None:
                    step['outputs'] = fixed
            except Exception:
                # Best-effort: never break the workflow if validation fails
                continue

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
        if not endpoints:
            return None

        # Extract potential identifiers from the step
        request = step.get('request') or {}
        operation_id = (
            step.get('operationId') or step.get('operation_id') or
            request.get('operationId') or request.get('operation_id')
        )
        method = (
            step.get('method') or request.get('method') or
            (step.get('endpoint') or {}).get('method') or
            (request.get('endpoint') or {}).get('method')
        )
        path = (
            step.get('path') or request.get('path') or
            (step.get('endpoint') or {}).get('path') or
            (request.get('endpoint') or {}).get('path') or
            request.get('url')  # sometimes "url" holds the path
        )

        # 1) Direct lookup by key (operationId or "METHOD path")
        if operation_id and operation_id in endpoints:
            return endpoints[operation_id]
        if method and path:
            key1 = f'{method.upper()} {path}'
            key2 = f'{method.lower()} {path}'
            if key1 in endpoints:
                return endpoints[key1]
            if key2 in endpoints:
                return endpoints[key2]

        # 2) Search by attributes inside endpoint data
        for _key, ep in endpoints.items():
            try:
                if operation_id and (ep.get('operationId') == operation_id or ep.get('operation_id') == operation_id):
                    return ep
                ep_method = (ep.get('method') or ep.get(
                    'httpMethod') or ep.get('http_method'))
                ep_path = (ep.get('path') or ep.get('url') or ep.get('route'))
                if method and path and ep_method and ep_path:
                    if str(ep_method).lower() == str(method).lower() and str(ep_path) == str(path):
                        return ep
            except Exception:
                continue

        # 3) Nothing found
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        # Try common structures from OpenAPI parsers
        responses = endpoint_data.get(
            'responses') or endpoint_data.get('response') or {}
        schema: dict[str, Any] = {}
        headers: dict[str, Any] = {}

        def pick_content_schema(resp: dict[str, Any]) -> dict[str, Any]:
            if not isinstance(resp, dict):
                return {}
            # OpenAPI 3: content -> mediaType -> schema
            content = resp.get('content')
            if isinstance(content, dict) and content:
                # Try application/json first, else first available
                if 'application/json' in content:
                    media = content['application/json']
                else:
                    media = next(iter(content.values()), {})
                if isinstance(media, dict):
                    return media.get('schema') or {}
            # OpenAPI 2: schema directly under response
            return resp.get('schema') or {}

        if isinstance(responses, dict) and responses:
            # Prefer 2xx
            preferred = None
            for code, resp in responses.items():
                try:
                    code_str = str(code)
                    if code_str.startswith('2'):
                        preferred = resp
                        # Prefer 200 if exists
                        if code_str == '200':
                            break
                except Exception:
                    continue
            if not preferred:
                # Fallback to any response
                preferred = next(iter(responses.values()),
                                 {}) if responses else {}

            schema = pick_content_schema(preferred) or {}
            headers = preferred.get('headers') or {}
        elif isinstance(responses, list):
            # List of response objects, pick first 2xx if possible
            preferred = None
            for resp in responses:
                code = str(resp.get('status') or resp.get('code') or '')
                if code.startswith('2'):
                    preferred = resp
                    if code == '200':
                        break
            if not preferred and responses:
                preferred = responses[0]
            if preferred:
                schema = pick_content_schema(preferred) or {}
                headers = preferred.get('headers') or {}

        # Additional common fields some parsers provide
        if not schema:
            schema = endpoint_data.get(
                'response_schema') or endpoint_data.get('schema') or {}
        if not headers:
            headers = endpoint_data.get(
                'response_headers') or endpoint_data.get('headers') or {}

        if not isinstance(schema, dict):
            schema = {}
        if not isinstance(headers, dict):
            headers = {}

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
        fixed: dict[str, str] = {}

        # Build flattened schema candidates and a set of normalized paths for validation
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}) if isinstance(schema, dict) else {})
        # If top-level schema is array, dive into items
        if not flat_schema and isinstance(schema, dict) and schema.get('type') == 'array' and isinstance(schema.get('items'), dict):
            flat_schema = OutputMappingValidator._flatten_schema(
                schema['items'].get('properties', {}))

        schema_paths = set()
        for path in set(flat_schema.values()):
            norm = OutputMappingValidator._normalize_property_path(path)
            schema_paths.add(norm)

        header_names = list(headers.keys()) if isinstance(
            headers, dict) else []
        # map normalized->canonical
        header_names_lower = {h.lower(): h for h in header_names}

        def parse_ref(ref: str) -> tuple[str | None, str]:
            s = ref.strip()
            # strip wrapping like ${...}
            if s.startswith('${') and s.endswith('}'):
                s = s[2:-1].strip()
            s_low = s.lower()

            loc = None
            if 'headers' in s_low:
                loc = 'headers'
            elif 'body' in s_low:
                loc = 'body'

            # extract path after '#/' if present
            if '#/' in s:
                path = s.split('#/', 1)[1]
            else:
                # try after 'headers' or 'body'
                if loc == 'headers':
                    path = re.split(
                        r'headers[\.#/]*', s, flags=re.IGNORECASE, maxsplit=1)[-1]
                elif loc == 'body':
                    path = re.split(r'body[\.#/]*', s,
                                    flags=re.IGNORECASE, maxsplit=1)[-1]
                else:
                    # attempt best-effort: take last segment after dot or slash
                    if '/' in s:
                        path = s.split('/')[-1]
                    elif '.' in s:
                        path = s.split('.')[-1]
                    else:
                        path = s
            path = path.strip().lstrip('/').strip()
            return loc, path

        def to_body_ref(path: str) -> str:
            p = path.lstrip('/').strip()
            return f'response.body#/{p}'

        def to_headers_ref(name: str) -> str:
            n = name.strip()
            return f'response.headers#/{n}'

        for out_name, out_ref in outputs.items():
            try:
                if not isinstance(out_ref, str) or not out_ref.strip():
                    # No reference provided, infer by best match
                    # Compare header best match vs body best match
                    # Header match
                    best_header_key = OutputMappingValidator._find_best_match(
                        out_name, header_names)
                    # Body match
                    best_schema_path = OutputMappingValidator._find_best_property_match(
                        out_name, flat_schema)

                    # Compute rough scores to decide preference
                    def norm_str(s: str) -> str:
                        return re.sub(r'[^a-z0-9]', '', s.lower())

                    header_score = 0.0
                    body_score = 0.0
                    if best_header_key:
                        header_score = difflib.SequenceMatcher(
                            None, norm_str(out_name), norm_str(best_header_key)).ratio()
                    if best_schema_path:
                        leaf = best_schema_path.split('/')[-1]
                        body_score = difflib.SequenceMatcher(
                            None, norm_str(out_name), norm_str(leaf)).ratio()

                    if header_score >= body_score and best_header_key:
                        fixed[out_name] = to_headers_ref(header_names_lower.get(
                            best_header_key.lower(), best_header_key))
                    elif best_schema_path:
                        fixed[out_name] = to_body_ref(best_schema_path)
                    else:
                        fixed[out_name] = out_ref  # keep unchanged
                    continue

                loc, path = parse_ref(out_ref)

                if loc == 'headers':
                    # Validate header exists; if not, find best match
                    canonical = header_names_lower.get(path.lower())
                    if canonical:
                        fixed[out_name] = to_headers_ref(canonical)
                        continue

                    best = OutputMappingValidator._find_best_match(
                        path, header_names)
                    if best:
                        fixed[out_name] = to_headers_ref(best)
                    else:
                        # Try to infer from the output name instead
                        best_from_name = OutputMappingValidator._find_best_match(
                            out_name, header_names)
                        if best_from_name:
                            fixed[out_name] = to_headers_ref(best_from_name)
                        else:
                            fixed[out_name] = out_ref  # give up; keep original

                else:
                    # default to body if not specified or body
                    # Validate and normalize property path
                    norm = OutputMappingValidator._normalize_property_path(
                        path)
                    if norm in schema_paths:
                        # Find the canonical flattened path that matches the normalized one
                        canonical_path = None
                        for p in flat_schema.values():
                            if OutputMappingValidator._normalize_property_path(p) == norm:
                                canonical_path = p
                                break
                        fixed[out_name] = to_body_ref(canonical_path or path)
                        continue

                    # Try to find best match from schema using output name first
                    best_schema_path = OutputMappingValidator._find_best_property_match(
                        out_name, flat_schema)
                    if not best_schema_path:
                        # Try from the provided path text
                        best_key = OutputMappingValidator._find_best_match(
                            path.split('/')[-1], list(flat_schema.keys()))
                        if best_key:
                            best_schema_path = flat_schema.get(best_key)

                    if best_schema_path:
                        fixed[out_name] = to_body_ref(best_schema_path)
                    else:
                        # Consider whether it was meant to be a header
                        best_header = OutputMappingValidator._find_best_match(
                            out_name, header_names)
                        if best_header:
                            fixed[out_name] = to_headers_ref(best_header)
                        else:
                            fixed[out_name] = out_ref  # keep unchanged
            except Exception:
                fixed[out_name] = out_ref

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
        s = path.strip()
        # Remove leading response/body/header markers and anchors
        s = re.sub(
            r'^(response\.)?(body|headers)[\.#/]*', '', s, flags=re.IGNORECASE)
        s = s.replace('#/', '/')
        s = s.lstrip('/')
        # Convert separators to dots
        s = s.replace('/', '.')
        # Remove array indices like [0], [1], etc.
        s = re.sub(r'\[\d+\]', '', s)
        # Replace multiple dots with single
        s = re.sub(r'\.{2,}', '.', s)
        return s

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

        def norm(s: str) -> str:
            # Normalize to improve likelihood of matching across styles
            s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', s)  # split camelCase
            return re.sub(r'[^a-z0-9]+', '', s1.lower())

        t = norm(target)
        best = None
        best_score = 0.0
        for c in candidates:
            score = difflib.SequenceMatcher(None, t, norm(c)).ratio()
            if score > best_score:
                best = c
                best_score = score

        # Require a minimal score to avoid spurious matches
        return best if best_score >= 0.55 else None

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

        # Prefer matches against property names, but include dotted keys as well
        candidates = list(flat_schema.keys())
        best_key = OutputMappingValidator._find_best_match(
            output_name, candidates)
        if best_key and best_key in flat_schema:
            return flat_schema[best_key]

        # If best_key was not in mapping (shouldn't happen), try fallback using leaf names
        leaf_to_path: dict[str, str] = {}
        for path in flat_schema.values():
            leaf = path.split('/')[-1]
            leaf_to_path[leaf] = path
        best_leaf = OutputMappingValidator._find_best_match(
            output_name, list(leaf_to_path.keys()))
        if best_leaf:
            return leaf_to_path[best_leaf]

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
        result: dict[str, str] = {}

        def add_candidate(name: str, full_path: str) -> None:
            # Map multiple candidate keys to the same full path for flexible matching
            # 1) raw property name
            result[name] = full_path
            # 2) dotted full path as a name candidate
            result[full_path.replace('/', '.')] = full_path
            # 3) snake_case-ish normalized name
            norm_name = re.sub(
                r'[^a-z0-9]+', '_', re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)).lower().strip('_')
            if norm_name:
                result[norm_name] = full_path

        def walk_props(props: dict[str, Any], pref: str) -> None:
            if not isinstance(props, dict):
                return
            for name, subschema in props.items():
                path = f'{pref}/{name}' if pref else name
                add_candidate(name, path)

                if isinstance(subschema, dict):
                    # Object with nested properties
                    if 'properties' in subschema and isinstance(subschema['properties'], dict):
                        walk_props(subschema['properties'], path)
                    # Array -> dive into items
                    items = subschema.get('items')
                    if isinstance(items, dict):
                        # Include the array element's properties under the same path
                        if 'properties' in items and isinstance(items['properties'], dict):
                            walk_props(items['properties'], path)

        walk_props(properties, prefix.strip('/'))
        return result
