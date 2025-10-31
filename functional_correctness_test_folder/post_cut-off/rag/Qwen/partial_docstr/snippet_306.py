
import re
from difflib import get_close_matches


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
        for step in workflow.get('steps', []):
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if endpoint_data:
                response_schema, response_headers = OutputMappingValidator._extract_response_info(
                    endpoint_data)
                step['outputs'] = OutputMappingValidator._validate_step_outputs(
                    step.get('outputs', {}), response_schema, response_headers)
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
        endpoint_id = step.get('endpoint_id')
        return endpoints.get(endpoint_id)

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        response_schema = {}
        response_headers = {}
        for response in endpoint_data.get('responses', {}).values():
            response_schema.update(response.get('content', {}).get(
                'application/json', {}).get('schema', {}).get('properties', {}))
            response_headers.update(response.get('headers', {}))
        return response_schema, response_headers

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
        flat_schema = OutputMappingValidator._flatten_schema(schema)
        flat_headers = {k: '' for k in headers.keys()}
        flat_schema.update(flat_headers)
        validated_outputs = {}
        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            best_match = OutputMappingValidator._find_best_property_match(
                normalized_path, flat_schema)
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
        return re.sub(r'\[\d+\]', '', path)

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        matches = get_close_matches(target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        '''Find the best matching property in the schema for an output name.
        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.
        Returns:
            The path to the matching property, or None if no match is found.
        '''
        return OutputMappingValidator._find_best_match(output_name, list(flat_schema.keys()))

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.
        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.
        Returns:
            A dictionary mapping property names to their paths.
        '''
        flat = {}
        for key, value in properties.items():
            path = f"{prefix}.{key}" if prefix else key
            if 'properties' in value:
                flat.update(OutputMappingValidator._flatten_schema(
                    value['properties'], path))
            else:
                flat[path] = path
        return flat
