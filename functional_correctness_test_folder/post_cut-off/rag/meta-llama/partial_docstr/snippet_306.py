
from typing import Any, Dict


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
    def _get_endpoint_for_step(step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Dict[str, Any] | None:
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
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        response_schema = {}
        response_headers = {}
        if 'responses' in endpoint_data:
            for status_code, response in endpoint_data['responses'].items():
                if 'content' in response:
                    for content_type, content in response['content'].items():
                        if 'schema' in content:
                            response_schema = content['schema']
                            break
                if 'headers' in response:
                    response_headers = response['headers']
        return response_schema, response_headers

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
        validated_outputs = {}
        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if normalized_path in flat_schema or normalized_path in headers:
                validated_outputs[output_name] = output_path
            else:
                best_match = OutputMappingValidator._find_best_property_match(
                    output_name, list(flat_schema.keys()))
                if best_match:
                    validated_outputs[output_name] = best_match
        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        '''Normalize a property path by removing array indices.
        Args:
            path: The property path to normalize.
        Returns:
            The normalized property path.
        '''
        return '.'.join([part.split('[')[0] for part in path.split('.')])

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        from difflib import SequenceMatcher
        if not candidates:
            return None
        best_match = max(candidates, key=lambda candidate: SequenceMatcher(
            None, target, candidate).ratio())
        return best_match

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> str | None:
        '''Find the best matching property in the schema for an output name.
        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.
        Returns:
            The path to the matching property, or None if no match is found.
        '''
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
        for property_name, property_schema in properties.items():
            property_path = f'{prefix}{property_name}' if prefix else property_name
            if 'properties' in property_schema:
                flat_schema.update(OutputMappingValidator._flatten_schema(
                    property_schema['properties'], property_path + '.'))
            else:
                flat_schema[property_path] = property_path
        return flat_schema
