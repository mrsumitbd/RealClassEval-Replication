
import re
import difflib
from typing import Any, Dict, List, Tuple, Optional


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(
        workflow: Dict[str, Any],
        openapi_spec: Dict[str, Any],
        endpoints: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Validate and fix output mappings in a workflow.
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
        # Work on a copy to avoid mutating the original
        validated = dict(workflow)

        # Assume workflow contains a list of steps under 'steps'
        steps = validated.get("steps", [])
        for step in steps:
            # Get the endpoint data for this step
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue

            # Extract response schema and headers
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)

            # Validate the step's outputs
            outputs = step.get("outputs", {})
            if outputs:
                validated_outputs = OutputMappingValidator._validate_step_outputs(
                    outputs, schema, headers
                )
                step["outputs"] = validated_outputs

        return validated

    @staticmethod
    def _get_endpoint_for_step(
        step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        """
        # Prefer explicit endpoint reference
        if "endpoint" in step:
            return endpoints.get(step["endpoint"])

        # Fallback: build key from method and path
        method = step.get("method", "").upper()
        path = step.get("path", "")
        if method and path:
            key = f"{method} {path}"
            return endpoints.get(key)

        return None

    @staticmethod
    def _extract_response_info(
        endpoint_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        """
        responses = endpoint_data.get("responses", {})
        # Prefer 200, then default, then any
        status_code = None
        for code in ("200", "default"):
            if code in responses:
                status_code = code
                break
        if not status_code:
            # Pick first available
            status_code = next(iter(responses), None)

        if not status_code:
            return {}, {}

        response = responses[status_code]
        # Extract schema from first content type
        schema = {}
        content = response.get("content", {})
        if content:
            # Pick first media type
            media_type = next(iter(content), None)
            if media_type:
                schema = content[media_type].get("schema", {})

        headers = response.get("headers", {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(
        outputs: Dict[str, str], schema: Dict[str, Any], headers: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Validate and fix output mappings for a step.
        Args:
            outputs: The output mappings to validate.
            schema: The response schema.
            headers: The response headers.
        Returns:
            The validated and fixed output mappings.
        """
        if not schema:
            return outputs

        # Flatten the schema properties
        flat_schema = {}
        if "properties" in schema:
            flat_schema = OutputMappingValidator._flatten_schema(
                schema["properties"])

        # Build a set of valid paths from schema and headers
        valid_paths = set()
        # Schema paths
        for path in flat_schema.values():
            valid_paths.add(path)
        # Header paths
        for header_name in headers:
            # Header names are case-insensitive; use lower-case
            valid_paths.add(header_name.lower())

        updated_outputs = {}
        for out_name, prop_path in outputs.items():
            norm_path = OutputMappingValidator._normalize_property_path(
                prop_path)
            if norm_path.lower() in valid_paths:
                updated_outputs[out_name] = prop_path
                continue

            # Try to find best match in schema properties
            best_match = OutputMappingValidator._find_best_property_match(
                out_name, flat_schema)
            if best_match:
                updated_outputs[out_name] = best_match
                continue

            # Try to find best match in headers
            header_match = OutputMappingValidator._find_best_match(
                out_name, list(headers.keys()))
            if header_match:
                updated_outputs[out_name] = header_match
                continue

            # If nothing found, keep original
            updated_outputs[out_name] = prop_path

        return updated_outputs

    @staticmethod
    def _normalize_property
