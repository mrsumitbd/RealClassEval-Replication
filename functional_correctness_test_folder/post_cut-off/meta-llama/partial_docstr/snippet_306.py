
from typing import Any, Dict, List, Tuple, Union


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''
    @staticmethod
    def validate_output_mappings(workflow: Dict[str, Any], openapi_spec: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
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
        for step_name, step in workflow.get('steps', {}).items():
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if endpoint_data:
                response_schema, response_headers = OutputMappingValidator._extract_response_info(
                    endpoint_data)
                if 'outputs' in step:
                    step['outputs'] = OutputMappingValidator._validate_step_outputs(
                        step['outputs'], response_schema, response_headers)
        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Union[Dict[str, Any], None]:
        '''Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        '''
        operation_id = step.get('operationId')
        if operation_id and operation_id in endpoints:
            return endpoints[operation_id]
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        responses = endpoint_data.get('responses', {})
        successful_response = next(
            (response for code, response in responses.items() if code.startswith('2')), None)
        if successful_response:
            schema = successful_response.get('content', {}).get(
                'application/json', {}).get('schema', {})
            headers = {header: details.get(
                'schema', {}) for header, details in successful_response.get('headers', {}).items()}
            return schema, headers
        return {}, {}

    @staticmethod
    def _validate_step_outputs(outputs: Dict[str, str], schema: Dict[str, Any], headers: Dict[str, Any]) -> Dict[str, str]:
        '''Validate and fix output mappings for a step.
        Args:
            outputs: The output mappings to validate.
            schema: The response schema.
            headers: The response headers.
        Returns:
            The validated and fixed output mappings.
        '''
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        flat_headers = {header: header for header in headers.keys()}
        validated_outputs = {}
        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if normalized_path in flat_schema:
                validated_outputs[output_name] = normalized_path
            elif normalized_path in flat_headers:
                validated_outputs[output_name] = normalized_path
            else:
                best_match = OutputMappingValidator._find_best_property_match(
                    output_name, {**flat_schema, **flat_headers})
                if best_match:
                    validated_outputs[output_name] = best_match
        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        return path.strip('/').replace('/', '.')

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Union[str, None]:
        best_match = None
        best_ratio = 0
        for candidate in candidates:
            ratio = OutputMappingValidator._calculate_similarity(
                target, candidate)
            if ratio > best_ratio:
                best_match = candidate
                best_ratio = ratio
        return best_match if best_ratio > 0.6 else None

    @staticmethod
    def _calculate_similarity(s1: str, s2: str) -> float:
        from difflib import SequenceMatcher
        return SequenceMatcher(None, s1, s2).ratio()

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> Union[str, None]:
        return OutputMappingValidator._find_best_match(output_name, list(flat_schema.keys()))

    @staticmethod
    def _flatten_schema(properties: Dict[str, Any], prefix: str = '') -> Dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.
        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.
        Returns:
            A dictionary mapping property names to their paths.
        '''
        flat_schema = {}
        for property_name, property_details in properties.items():
            property_path = f'{prefix}{property_name}' if prefix else property_name
            if 'properties' in property_details:
                flat_schema.update(OutputMappingValidator._flatten_schema(
                    property_details['properties'], property_path + '.'))
            else:
                flat_schema[property_path] = property_path
        return flat_schema
