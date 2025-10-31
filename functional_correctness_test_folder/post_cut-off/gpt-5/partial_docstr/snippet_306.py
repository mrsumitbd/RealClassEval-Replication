from __future__ import annotations

from typing import Any
import copy
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
        fixed_workflow = copy.deepcopy(workflow)

        def process_step(step: dict[str, Any]) -> None:
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                return
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            if not isinstance(step.get('outputs'), dict):
                # If no outputs mapping exists but schema is available, try to initialize a sensible default mapping
                step_outputs: dict[str, str] = {}
            else:
                step_outputs = step['outputs']

            fixed_outputs = OutputMappingValidator._validate_step_outputs(
                step_outputs, schema, headers)
            if fixed_outputs:
                step['outputs'] = fixed_outputs

        def walk(node: Any) -> None:
            if isinstance(node, dict):
                # A step can be a dict that might contain 'steps' or be a step itself
                if 'steps' in node and isinstance(node['steps'], list):
                    for s in node['steps']:
                        walk(s)
                # Some Arazzo structures might have nested branches like 'onSuccess', 'onFailure'
                for key in ('onSuccess', 'onFailure', 'then', 'else'):
                    if key in node:
                        walk(node[key])
                # Try process this node as a step
                if any(k in node for k in ('request', 'apiCall', 'operationId', 'operation')) or isinstance(node.get('outputs'), dict):
                    process_step(node)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        # Attempt common top-level containers
        if isinstance(fixed_workflow, dict):
            # Standard: workflow -> steps
            if 'workflow' in fixed_workflow and isinstance(fixed_workflow['workflow'], dict):
                wf = fixed_workflow['workflow']
                if 'steps' in wf:
                    walk(wf['steps'])
                else:
                    walk(wf)
            elif 'steps' in fixed_workflow:
                walk(fixed_workflow['steps'])
            else:
                walk(fixed_workflow)

        return fixed_workflow

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        '''Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        '''
        # Try common fields to retrieve operationId
        op_id = None
        if isinstance(step.get('request'), dict):
            op_id = step['request'].get(
                'operationId') or step['request'].get('operation_id')
        if not op_id and isinstance(step.get('apiCall'), dict):
            op_id = step['apiCall'].get(
                'operationId') or step['apiCall'].get('operation_id')
        if not op_id:
            op_id = step.get('operationId') or step.get('operation_id')
        if not op_id and isinstance(step.get('operation'), dict):
            op_id = step['operation'].get(
                'operationId') or step['operation'].get('operation_id')

        # Direct lookup by operationId
        if op_id and op_id in endpoints:
            return endpoints[op_id]

        # Some parsers store endpoints keyed by path/method; try to search by stored operationId
        if op_id:
            for key, ep in endpoints.items():
                if isinstance(ep, dict) and ep.get('operationId') == op_id:
                    return ep

        # Try path + method fields if provided
        path = None
        method = None
        if isinstance(step.get('request'), dict):
            path = step['request'].get('path')
            method = (step['request'].get('method') or '').lower() or None
        if not path and isinstance(step.get('apiCall'), dict):
            path = step['apiCall'].get('path')
            method = (step['apiCall'].get('method') or '').lower() or method

        if path and method:
            # endpoints might be {"/pets": {"get": {...}}}
            if path in endpoints and isinstance(endpoints[path], dict):
                method_data = endpoints[path].get(method)
                if isinstance(method_data, dict):
                    return method_data
            # endpoints might be {("/pets","get"): {...}}
            for key, ep in endpoints.items():
                if isinstance(key, tuple) and len(key) == 2 and key[0] == path and str(key[1]).lower() == method:
                    return ep

        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        # Prefer already processed shapes
        if 'response' in endpoint_data and isinstance(endpoint_data['response'], dict):
            resp = endpoint_data['response']
            schema = resp.get('schema') or resp.get('content') or {}
            headers = resp.get('headers') or {}
            # If schema nested under content
            if isinstance(schema, dict) and 'content' in schema and isinstance(schema['content'], dict):
                media = schema['content'].get(
                    'application/json') or next(iter(schema['content'].values()), {})
                schema = media.get('schema') or {}
            return (schema if isinstance(schema, dict) else {}), (headers if isinstance(headers, dict) else {})

        responses = endpoint_data.get('responses') if isinstance(
            endpoint_data.get('responses'), dict) else None
        if not responses and 'operation' in endpoint_data and isinstance(endpoint_data['operation'], dict):
            responses = endpoint_data['operation'].get('responses')

        responses = responses or {}

        # Choose a 2xx or default response
        preferred_codes = ['200', '201', '202', '204']
        chosen = None
        for code in preferred_codes:
            if code in responses:
                chosen = responses[code]
                break
        if not chosen:
            # First 2xx
            for code, resp in responses.items():
                try:
                    if str(code).startswith('2'):
                        chosen = resp
                        break
                except Exception:
                    continue
        if not chosen:
            chosen = responses.get('default') or {}

        if not isinstance(chosen, dict):
            return {}, {}

        headers = chosen.get('headers') if isinstance(
            chosen.get('headers'), dict) else {}
        schema: dict[str, Any] = {}

        # OpenAPI v3 content
        content = chosen.get('content')
        if isinstance(content, dict) and content:
            media = content.get(
                'application/json') or next(iter(content.values()), {})
            if isinstance(media, dict):
                schema = media.get('schema') if isinstance(
                    media.get('schema'), dict) else {}
        else:
            # OpenAPI v2 (swagger) may have 'schema' directly
            if isinstance(chosen.get('schema'), dict):
                schema = chosen['schema']

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
        fixed = dict(outputs or {})

        # Build flattened body properties
        body_flat: dict[str, str] = {}
        if isinstance(schema, dict):
            props = schema.get('properties')
            if not isinstance(props, dict):
                # If top-level schema is an array or direct type, treat top-level as 'body'
                if schema.get('type') == 'object' and isinstance(schema.get('properties'), dict):
                    props = schema.get('properties')
                else:
                    props = {}
            body_flat = OutputMappingValidator._flatten_schema(
                props, prefix='body.')

        header_names = list(headers.keys()) if isinstance(
            headers, dict) else []
        normalized_header_names = [h.lower() for h in header_names]

        # Validate existing mappings
        for out_name, mapping in list(fixed.items()):
            if not isinstance(mapping, str) or not mapping.strip():
                # We'll try to infer later
                continue
            norm = OutputMappingValidator._normalize_property_path(mapping)
            if norm.startswith('headers.'):
                hdr = norm.split('.', 1)[1]
                if hdr.lower() not in normalized_header_names:
                    best = OutputMappingValidator._find_best_match(
                        hdr, header_names)
                    if best:
                        fixed[out_name] = f'$.headers.{best}'
                    else:
                        # Leave as-is
                        fixed[out_name] = f'$.headers.{hdr}'
                else:
                    # Normalize to JSONPath
                    # Use original header casing if present
                    if hdr.lower() in normalized_header_names:
                        idx = normalized_header_names.index(hdr.lower())
                        fixed[out_name] = f'$.headers.{header_names[idx]}'
                    else:
                        fixed[out_name] = f'$.headers.{hdr}'
            else:
                # Body mapping
                # Verify property path exists
                candidates = set(body_flat.values())
                if norm not in candidates:
                    # Try find best match by full path
                    best_path = OutputMappingValidator._find_best_match(
                        norm, list(candidates))
                    if not best_path:
                        # Try match by output name to property names
                        best_path = OutputMappingValidator._find_best_property_match(
                            out_name, body_flat)
                    if best_path:
                        fixed[out_name] = f'$.{best_path}'
                    else:
                        # leave normalized original
                        fixed[out_name] = f'$.{norm}'
                else:
                    fixed[out_name] = f'$.{norm}'

        # For missing mappings try to infer from output name
        for out_name, mapping in list(fixed.items()):
            if mapping:
                continue
            best = OutputMappingValidator._find_best_property_match(
                out_name, body_flat)
            if best:
                fixed[out_name] = f'$.{best}'

        return fixed

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        if not isinstance(path, str):
            return ''
        p = path.strip()
        # Remove leading JSONPath symbols
        if p.startswith('$.'):
            p = p[2:]
        elif p.startswith('$'):
            p = p[1:]
        if p.startswith('/'):
            p = p.lstrip('/').replace('/', '.')
        # Common aliases
        if p.lower().startswith('response.'):
            p = 'body.' + p.split('.', 1)[1]
        if p.startswith('body['):
            p = p.replace('body[', 'body.').replace(']', '')
        if p.startswith('headers['):
            p = p.replace('headers[', 'headers.').replace(']', '')
        # If neither headers nor body specified, assume body
        if not (p.startswith('body.') or p.startswith('headers.')):
            p = 'body.' + p.lstrip('.')
        # Normalize consecutive dots
        while '..' in p:
            p = p.replace('..', '.')
        # Strip trailing dot
        p = p.strip('.')
        return p

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        if not target or not candidates:
            return None
        # Exact (case-insensitive)
        lower_map = {c.lower(): c for c in candidates}
        if target.lower() in lower_map:
            return lower_map[target.lower()]
        # Use difflib for fuzzy match
        best = difflib.get_close_matches(target, candidates, n=1, cutoff=0.6)
        if best:
            return best[0]
        # Try match by last segment
        last = target.split('.')[-1].lower()
        for c in candidates:
            if c.lower().endswith(last):
                return c
        return None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        if not output_name or not flat_schema:
            return None
        names = list(flat_schema.keys())
        # Direct or case-insensitive
        if output_name in flat_schema:
            return flat_schema[output_name]
        if output_name.lower() in {k.lower() for k in names}:
            for k in names:
                if k.lower() == output_name.lower():
                    return flat_schema[k]
        # Fuzzy
        best_name = OutputMappingValidator._find_best_match(output_name, names)
        if best_name:
            return flat_schema.get(best_name)
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

        def add(name: str, full_path: str) -> None:
            if name not in flat:
                flat[name] = full_path

        def walk(schema: dict[str, Any], cur_path: str) -> None:
            if not isinstance(schema, dict):
                return
            typ = schema.get('type')
            if typ == 'object' or ('properties' in schema and isinstance(schema.get('properties'), dict)):
                props = schema.get('properties', {})
                for prop_name, prop_schema in props.items():
                    next_path = f'{cur_path}{prop_name}'
                    add(prop_name, next_path)
                    # Recurse for nested objects/arrays
                    if isinstance(prop_schema, dict):
                        ptype = prop_schema.get('type')
                        if ptype == 'object' or isinstance(prop_schema.get('properties'), dict):
                            walk(prop_schema, next_path + '.')
                        elif ptype == 'array' and isinstance(prop_schema.get('items'), dict):
                            # For arrays, include the property itself and dive into items
                            add(prop_name, next_path)  # already added
                            items = prop_schema.get('items', {})
                            # Represent nested items with same path for matching by name
                            if isinstance(items, dict):
                                if items.get('type') == 'object' or isinstance(items.get('properties'), dict):
                                    walk(items, next_path + '.')
                                else:
                                    # Primitive array items; nothing further
                                    pass
            elif typ == 'array' and isinstance(schema.get('items'), dict):
                items = schema['items']
                walk(items, cur_path)

        if isinstance(properties, dict):
            wrapper_schema = {'type': 'object', 'properties': properties}
            walk(wrapper_schema, prefix)

        return flat
