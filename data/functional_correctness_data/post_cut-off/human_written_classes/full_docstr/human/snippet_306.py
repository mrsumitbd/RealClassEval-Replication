from typing import Any
import difflib
from Levenshtein import distance

class OutputMappingValidator:
    """Validates and fixes output mappings in Arazzo workflows."""

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """Validate and fix output mappings in a workflow.

        This function checks all output mappings in a workflow against the
        corresponding response schemas from the OpenAPI spec and fixes any
        inconsistencies.

        Args:
            workflow: The workflow to validate.
            openapi_spec: The OpenAPI specification.
            endpoints: Dictionary of endpoints from the OpenAPI parser.

        Returns:
            The validated and fixed workflow.
        """
        if not workflow or 'steps' not in workflow:
            return workflow
        for step in workflow['steps']:
            if 'outputs' not in step:
                continue
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(step, endpoints)
            if not endpoint_data:
                logger.warning(f"Could not find endpoint for step: {step.get('stepId', 'unknown')}")
                continue
            response_schema, response_headers = OutputMappingValidator._extract_response_info(endpoint_data)
            step['outputs'] = OutputMappingValidator._validate_step_outputs(step['outputs'], response_schema, response_headers)
        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        """Get the endpoint data for a step.

        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.

        Returns:
            The endpoint data or None if not found.
        """
        if 'operationId' in step:
            operation_id = step['operationId']
            for path_data in endpoints.values():
                for endpoint_data in path_data.values():
                    if endpoint_data.get('operation_id') == operation_id:
                        return endpoint_data
        if 'operationPath' in step:
            operation_path = step['operationPath']
            if operation_path.startswith('openapi_source#/paths/'):
                parts = operation_path.split('/paths/', 1)[1].rsplit('/', 1)
                if len(parts) == 2:
                    path = '/' + parts[0].replace('~1', '/')
                    method = parts[1]
                    if path in endpoints and method in endpoints[path]:
                        return endpoints[path][method]
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        """Extract response schema and headers from endpoint data.

        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.

        Returns:
            A tuple of (response_schema, response_headers).
        """
        response_schema = {}
        response_headers = {}
        responses = endpoint_data.get('responses', {})
        success_codes = []
        for code in responses.keys():
            if isinstance(code, str | int) and str(code).startswith('2'):
                success_codes.append(code)
        for code in success_codes:
            response_data = responses.get(str(code), {})
            content = response_data.get('content', {})
            for content_data in content.values():
                if 'schema' in content_data:
                    schema = content_data['schema']
                    if schema.get('type') == 'array' and 'items' in schema:
                        items_schema = schema['items']
                        response_schema = {'type': 'array', 'is_array': True}
                        if 'properties' in items_schema:
                            response_schema['item_properties'] = items_schema.get('properties', {})
                    elif 'properties' in schema:
                        response_schema = schema
                    break
            headers = response_data.get('headers', {})
            if headers:
                response_headers = headers
            if response_schema and response_headers:
                break
        return (response_schema, response_headers)

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        """Validate and fix output mappings for a step.

        Args:
            outputs: The output mappings to validate.
            schema: The response schema.
            headers: The response headers.

        Returns:
            The validated and fixed output mappings.
        """
        if not outputs:
            return outputs
        validated_outputs = {}
        is_array_response = schema.get('type') == 'array' and schema.get('is_array', False)
        if is_array_response and 'item_properties' in schema:
            properties = schema.get('item_properties', {})
        else:
            properties = schema.get('properties', {})
        flat_schema = OutputMappingValidator._flatten_schema(properties)
        header_schema = {}
        for header_name in headers:
            header_schema[header_name] = f'$response.headers.{header_name}'
        for output_name, output_path in outputs.items():
            if not output_path.startswith('$response'):
                validated_outputs[output_name] = output_path
                continue
            if output_path.startswith('$response.headers.'):
                header_name = output_path[len('$response.headers.'):]
                if header_name in header_schema:
                    validated_outputs[output_name] = output_path
                else:
                    best_match = OutputMappingValidator._find_best_match(header_name, list(header_schema.keys()))
                    if best_match:
                        logger.warning(f"Fixing invalid header reference: '{header_name}' -> '{best_match}'")
                        validated_outputs[output_name] = f'$response.headers.{best_match}'
                    else:
                        validated_outputs[output_name] = output_path
            elif output_path.startswith('$response.body'):
                property_path = output_path[len('$response.body'):]
                if not property_path or property_path == '#':
                    validated_outputs[output_name] = output_path
                    continue
                normalized_path = OutputMappingValidator._normalize_property_path(property_path)
                if normalized_path in flat_schema.values():
                    validated_outputs[output_name] = output_path
                else:
                    prop_name = property_path.split('/')[-1]
                    best_path = OutputMappingValidator._find_best_property_match(prop_name, flat_schema)
                    if best_path:
                        if is_array_response and (not any((segment.isdigit() for segment in best_path.split('/')))):
                            if best_path.startswith('#/'):
                                best_path = f'#/0{best_path[1:]}'
                            else:
                                best_path = f'#/0{best_path}'
                        logger.warning(f"Fixing invalid property reference: '{property_path}' -> '{best_path}'")
                        validated_outputs[output_name] = f'$response.body{best_path}'
                    else:
                        validated_outputs[output_name] = output_path
            else:
                validated_outputs[output_name] = output_path
        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        """Normalize a property path by removing array indices.

        Args:
            path: The property path to normalize.

        Returns:
            The normalized property path.
        """
        if not path:
            return path
        segments = path.split('/')
        normalized_segments = []
        for segment in segments:
            if not segment.isdigit():
                normalized_segments.append(segment)
        return '/'.join(normalized_segments)

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        """Find the best matching string from a list of candidates using sequence matching.

        Args:
            target: The target string to match.
            candidates: List of candidate strings.

        Returns:
            The best matching string or None if candidates is empty.
        """
        if not candidates:
            return None
        similarities = [(candidate, difflib.SequenceMatcher(None, target, candidate).ratio()) for candidate in candidates]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[0][0]

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        """Find the best matching property in the schema for an output name.

        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.

        Returns:
            The path to the matching property, or None if no match is found.
        """
        for prop_name, path in flat_schema.items():
            if output_name == prop_name:
                return path
        normalized_output = output_name.lower().replace('_', '').replace('-', '')
        for prop_name, path in flat_schema.items():
            normalized_prop = prop_name.lower().replace('_', '').replace('-', '')
            if normalized_output == normalized_prop:
                return path
        if output_name.endswith('_id'):
            for prop_name, path in flat_schema.items():
                if prop_name == 'id':
                    return path
        best_match = None
        best_score = 0
        for prop_name, path in flat_schema.items():
            distance_value = distance(output_name.lower(), prop_name.lower())
            max_len = max(len(output_name), len(prop_name))
            score = 1 - distance_value / max_len if max_len > 0 else 0
            if score > best_score and score > 0.7:
                best_score = score
                best_match = path
        return best_match

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str='') -> dict[str, str]:
        """Flatten a nested schema into a dictionary of property paths.

        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.

        Returns:
            A dictionary mapping property names to their paths.
        """
        result = {}
        for prop_name, prop_schema in properties.items():
            if not prefix:
                path = f'#/{prop_name}'
            else:
                path = f'{prefix}/{prop_name}'
            result[prop_name] = path
            if prop_schema.get('type') == 'object' and 'properties' in prop_schema:
                nested = OutputMappingValidator._flatten_schema(prop_schema['properties'], path)
                result.update(nested)
            if prop_schema.get('type') == 'array' and 'items' in prop_schema:
                items = prop_schema['items']
                if items.get('type') == 'object' and 'properties' in items:
                    array_path = f'{path}/0'
                    nested = OutputMappingValidator._flatten_schema(items['properties'], array_path)
                    result.update(nested)
        return result