
import re
from difflib import SequenceMatcher
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
                response_schema, response_headers = OutputMappingValidator._extract_response_info(
                    endpoint_data)
                if 'outputs' in step:
                    step['outputs'] = OutputMappingValidator._validate_step_outputs(
                        step['outputs'], response_schema, response_headers)
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
        if 'endpoint' in step:
            return endpoints.get(step['endpoint'])
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        responses = endpoint_data.get('responses', {})
        default_response = responses.get('default', {})
        content = default_response.get('content', {})
        json_content = content.get('application/json', {})
        schema = json_content.get('schema', {})
        headers = default_response.get('headers', {})
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
        validated_outputs = {}
        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if normalized_path in flat_schema:
                validated_outputs[output_name] = normalized_path
            else:
                best_match = OutputMappingValidator._find_best_property_match(
                    output_name, flat_schema)
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
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates:
            return None
        matches = [(candidate, SequenceMatcher(None, target, candidate).ratio())
                   for candidate in candidates]
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0][0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> Optional[str]:
        '''Find the best matching property in the schema for an output name.
        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.
        Returns:
            The path to the matching property, or None if no match is found.
        '''
        schema_properties = list(flat_schema.keys())
        best_match = OutputMappingValidator._find_best_match(
            output_name, schema_properties)
        return flat_schema.get(best_match) if best_match else None

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
        for prop_name, prop_def in properties.items():
            current_path = f"{prefix}.{prop_name}" if prefix else prop_name
            if prop_def.get('type') == 'object' and 'properties' in prop_def:
                nested_schema = OutputMappingValidator._flatten_schema(
                    prop_def['properties'], current_path)
                flat_schema.update(nested_schema)
            else:
                flat_schema[prop_name] = current_path
        return flat_schema
