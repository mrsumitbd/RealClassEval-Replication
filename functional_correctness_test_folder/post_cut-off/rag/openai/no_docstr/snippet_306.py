
import difflib
import re
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
            # Get the endpoint data for this step.
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                # If we cannot find an endpoint, skip validation for this step.
                continue

            # Extract the response schema and headers.
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)

            # Flatten the schema to get a mapping of property names to paths.
            flat_schema = OutputMappingValidator._flatten_schema(
                schema.get("properties", {}))

            # Validate the outputs for this step.
            outputs = step.get("outputs", {})
            if isinstance(outputs, dict):
                validated_outputs = OutputMappingValidator._validate_step_outputs(
                    outputs, schema, headers
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
        # Prefer explicit endpoint reference.
        endpoint_name = step.get("endpoint")
        if endpoint_name and endpoint_name in endpoints:
            return endpoints[endpoint_name]

        # Fallback: match by method and path.
        method = step.get("method")
        path = step.get("path")
        if method and path:
            for ep in endpoints.values():
                if ep.get("method", "").lower() == method.lower() and ep.get("path") == path:
                    return ep
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
        # Prefer 200, otherwise first status code.
        response_obj = None
        if "200" in responses:
            response_obj = responses["200"]
        elif responses:
            # Pick the first status code.
            response_obj = next(iter(responses.values()))

        schema = {}
        headers = {}
        if response_obj:
            # Extract JSON schema.
            content = response_obj.get("content", {})
            json_content = content.get("application/json", {})
            schema = json_content.get("schema", {})
            # Extract headers if present.
            headers = response_obj.get("headers", {})
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
        # Flatten schema to get property paths.
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        # Build a set of valid paths (normalized).
        valid_paths = {OutputMappingValidator._normalize_property_path(
            p) for p in flat_schema.values()}

        # Build a set of header keys (normalized).
        valid_headers = {OutputMappingValidator._normalize_property_path(
            h) for h in headers.keys()}

        validated = {}
        for out_name, prop_path in outputs.items():
            norm_path = OutputMappingValidator._normalize_property_path(
                prop_path)

            # If the path is already valid, keep it.
            if norm_path in valid_paths or norm_path in valid_headers:
                validated[out_name] = prop_path
                continue

            # Try to find the best match in schema paths.
            best_match = OutputMappingValidator._find_best_match(
                norm_path, list(valid_paths))
            if best_match:
                # Find the original path that matches this normalized path.
                for orig_path in flat_schema.values():
                    if OutputMappingValidator._normalize_property_path(orig_path) == best_match:
                        validated[out_name] = orig_path
                        break
                continue

            # Try to find the best match in headers.
            best_header = OutputMappingValidator._find_best_match(
                norm_path, list(valid_headers))
            if best_header:
                # Find the original header key.
                for hdr in headers.keys():
                    if OutputMappingValidator._normalize_property_path(hdr) == best_header:
                        validated[out_name] = hdr
