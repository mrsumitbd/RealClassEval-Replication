
from typing import Any, Dict, Optional, Tuple, List
import difflib


class OutputMappingValidator:
    """Validates and fixes output mappings in Arazzo workflows."""

    @staticmethod
    def validate_output_mappings(workflow: Dict[str, Any], openapi_spec: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
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
    def _get_endpoint_for_step(step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Get the endpoint data for a step.

        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.

        Returns:
            The endpoint data or None if not found.
        """
        if 'operationId' not in step:
            return None
        return endpoints.get(step['operationId'])

    @staticmethod
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Extract response schema and headers from endpoint data.

        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.

        Returns:
            A tuple of (response_schema, response_headers).
        """
        responses = endpoint_data.get('responses', {})
        success_response = responses.get('200', responses.get('default', {}))
        schema = success_response.get('content', {}).get(
            'application/json', {}).get('schema', {})
        headers = success_response.get('headers', {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: Dict[str, str], schema: Dict[str, Any], headers: Dict[str, Any]) -> Dict[str, str]:
        """Validate and fix output mappings for a step.

        Args:
            outputs: The output mappings to validate.
            schema: The response schema.
            headers: The response headers.

        Returns:
            The validated and fixed output mappings.
        """
        if not schema and not headers:
            return outputs

        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        flat_headers = {k.lower(): f"headers.{k}" for k in headers.keys()}

        validated_outputs = {}
        for output_name, path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                path)

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
                best_match = OutputMappingValidator._find_best_property_match(
                    output_name, flat_schema)
                if best_match:
                    validated_outputs[output_name] = best_match

        return validated_outputs or outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        """Normalize a property path by removing array indices.

        Args:
            path: The property path to normalize.

        Returns:
            The normalized property path.
        """
        return path.replace('[0]', '').replace('[]', '')

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        """Find the best matching string from a list of candidates using sequence matching.

        Args:
            target: The target string to match.
            candidates: List of candidate strings.

        Returns:
            The best matching string or None if candidates is empty.
        """
        if not candidates:
            return None
        matches = difflib.get_close_matches(
            target.lower(), [c.lower() for c in candidates], n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> Optional[str]:
        """Find the best matching property in the schema for an output name.

        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.

        Returns:
            The path to the matching property, or None if no match is found.
        """
        best_match = OutputMappingValidator._find_best_match(
            output_name, list(flat_schema.keys()))
        return flat_schema[best_match] if best_match else None

    @staticmethod
    def _flatten_schema(properties: Dict[str, Any], prefix: str = '') -> Dict[str, str]:
        """Flatten a nested schema into a dictionary of property paths.

        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.

        Returns:
            A dictionary mapping property names to their paths.
        """
        flat = {}
        for prop, details in properties.items():
            current_path = f"{prefix}.{prop}" if prefix else prop
            if 'properties' in details:
                flat.update(OutputMappingValidator._flatten_schema(
                    details['properties'], current_path))
            else:
                flat[prop] = current_path
        return flat
