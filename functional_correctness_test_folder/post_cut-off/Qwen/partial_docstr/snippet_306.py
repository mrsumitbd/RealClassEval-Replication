
from typing import Any, Dict, List, Optional, Tuple


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
        for step in workflow.get('steps', []):
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if endpoint_data:
                schema, headers = OutputMappingValidator._extract_response_info(
                    endpoint_data)
                step['outputs'] = OutputMappingValidator._validate_step_outputs(
                    step.get('outputs', {}), schema, headers)
        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        '''Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        '''
        endpoint_id = step.get('endpoint_id')
        return endpoints.get(endpoint_id)

    @staticmethod
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        '''Extract the response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data.
        Returns:
            A tuple containing the response schema and headers.
        '''
        responses = endpoint_data.get('responses', {})
        # Assuming 200 is the success response
        response_data = responses.get('200', {})
        schema = response_data.get('content', {}).get(
            'application/json', {}).get('schema', {})
        headers = response_data.get('headers', {})
        return schema, headers

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
        flat_headers = {k: '' for k in headers.keys()}
        flat_schema.update(flat_headers)
        validated_outputs = {}
        for output_name, path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                path)
            best_match = OutputMappingValidator._find_best_property_match(
                output_name, flat_schema)
            if best_match:
                validated_outputs[output_name] = best_match
        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        '''Normalize a property path.
        Args:
            path: The property path to normalize.
        Returns:
            The normalized property path.
        '''
        return path.strip('/').replace('/', '.')

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        '''Find the best match for a target string in a list of candidates.
        Args:
            target: The target string to match.
            candidates: The list of candidate strings.
        Returns:
            The best matching string or None if no match is found.
        '''
        for candidate in candidates:
            if target.lower() == candidate.lower():
                return candidate
        return None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> Optional[str]:
        '''Find the best property match for an output name in a flattened schema.
        Args:
            output_name: The output name to match.
            flat_schema: The flattened schema.
        Returns:
            The best matching property path or None if no match is found.
        '''
        candidates = list(flat_schema.keys())
        return OutputMappingValidator._find_best_match(output_name, candidates)

    @staticmethod
    def _flatten_schema(properties: Dict[str, Any], prefix: str = '') -> Dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.
        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.
        Returns:
            A dictionary mapping property names to their paths.
        '''
        flat = {}
        for key, value in properties.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if 'properties' in value:
                flat.update(OutputMappingValidator._flatten_schema(
                    value['properties'], full_key))
            else:
                flat[full_key] = full_key
        return flat
