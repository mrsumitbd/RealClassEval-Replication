
import re
import difflib
from typing import Any, Dict, List, Tuple, Optional


class OutputMappingValidator:
    """Validates and fixes output mappings in Arazzo workflows."""

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
        # The workflow is expected to contain a list of steps under the key "steps".
        steps = workflow.get("steps", [])
        for step in steps:
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue

            response_schema, response_headers = OutputMappingValidator._extract_response_info(
                endpoint_data
            )
            if not response_schema:
                continue

            # Flatten the schema to get property paths
            flat_schema = OutputMappingValidator._flatten_schema(
                response_schema.get("properties", {}))

            # Validate the outputs for this step
            outputs = step.get("outputs", {})
            if outputs:
                validated_outputs = OutputMappingValidator._validate_step_outputs(
                    outputs, response_schema, response_headers
                )
                step["outputs"] = validated_outputs

        return workflow

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
        # Prefer operationId if present, otherwise use a generic key
        operation_id = step.get("operationId") or step.get("endpoint")
        if not operation_id:
            return None
        return endpoints.get(operation_id)

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
        # Prefer 200, then default, then any status code
        response = (
            responses.get("200")
            or responses.get("default")
            or next(iter(responses.values()), {})
        )
        # Extract JSON schema
        content = response.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        # Extract headers
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
        # Flatten schema to get property paths
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        # Normalize header names for matching
        header_names = {h.lower(): h for h in headers.keys()}

        validated: Dict[str, str] = {}
        for out_name, path in outputs.items():
            # Normalize the path (remove array indices)
            norm_path = OutputMappingValidator._normalize_property_path(path)

            # Check if the path exists in the schema (by value)
            if norm_path in flat_schema.values():
                validated[out_name] = path
                continue

            # Check if the path matches a header name
            if norm_path.lower() in
