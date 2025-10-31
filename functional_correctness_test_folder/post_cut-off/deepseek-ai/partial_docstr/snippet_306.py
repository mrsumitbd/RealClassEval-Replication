
from typing import Any, Optional, Tuple, Dict, List


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
        if 'steps' not in workflow:
            return workflow

        for step in workflow['steps']:
            if 'outputs' not in step:
                continue
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            step['outputs'] = OutputMappingValidator._validate_step_outputs(
                step['outputs'], schema, headers)

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
        if 'endpoint' not in step:
            return None
        return endpoints.get(step['endpoint'])

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        schema = {}
        headers = {}
        if 'responses' in endpoint_data:
            for response in endpoint_data['responses'].values():
                if 'content' in response and 'application/json' in response['content']:
                    schema = response['content']['application/json'].get(
                        'schema', {})
                if 'headers' in response:
                    headers = response['headers']
                break  # Only consider the first response
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
        validated_outputs = {}
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        flat_headers = {
            header.lower(): f"headers.{header}" for header in headers.keys()}

        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if normalized_path.startswith('headers.'):
                header_name = normalized_path.split('.')[1].lower()
                if header_name in flat_headers:
                    validated_outputs[output_name] = flat_headers[header_name]
                else:
                    best_match = OutputMappingValidator._find_best_match(
                        header_name, list(flat_headers.keys()))
                    if best_match:
                        validated_outputs[output_name] = flat_headers[best_match]
            else:
                if normalized_path in flat_schema.values():
                    validated_outputs[output_name] = normalized_path
                else:
                    best_match = OutputMappingValidator._find_best_property_match(
                        output_name, flat_schema)
                    if best_match:
                        validated_outputs[output_name] = best_match

        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        return path.strip().replace('$.', '').replace('.[', '[').replace('..', '.').strip('.')

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        if not candidates:
            return None
        target_lower = target.lower()
        for candidate in candidates:
            if candidate.lower() == target_lower:
                return candidate
        for candidate in candidates:
            if target_lower in candidate.lower() or candidate.lower() in target_lower:
                return candidate
        return None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        if not flat_schema:
            return None
        output_lower = output_name.lower()
        for prop_name, prop_path in flat_schema.items():
            if prop_name.lower() == output_lower:
                return prop_path
        for prop_name, prop_path in flat_schema.items():
            if output_lower in prop_name.lower() or prop_name.lower() in output_lower:
                return prop_path
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
        flat = {}
        for prop_name, prop_data in properties.items():
            current_path = f"{prefix}.{prop_name}" if prefix else prop_name
            if 'properties' in prop_data:
                flat.update(OutputMappingValidator._flatten_schema(
                    prop_data['properties'], current_path))
            else:
                flat[prop_name] = current_path
        return flat
