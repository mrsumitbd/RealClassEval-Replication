
from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional
import difflib


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(
        workflow: dict[str, Any],
        openapi_spec: dict[str, Any],
        endpoints: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
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
        # Assume workflow has a 'steps' key mapping step names to step dicts
        steps = workflow.get("steps", {})
        for step_name, step in steps.items():
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            if not schema:
                continue
            outputs = step.get("outputs", {})
            if not isinstance(outputs, dict):
                continue
            fixed_outputs = OutputMappingValidator._validate_step_outputs(
                outputs, schema, headers)
            step["outputs"] = fixed_outputs
        return workflow

    @staticmethod
    def _get_endpoint_for_step(
        step: dict[str, Any], endpoints: dict[str, dict[str, Any]]
    ) -> Optional[dict[str, Any]]:
        """
        Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        """
        # The step is expected to reference an endpoint by name or operationId
        endpoint_key = step.get("endpoint") or step.get("operationId")
        if not endpoint_key:
            return None
        return endpoints.get(endpoint_key)

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> Tuple[Optional[dict[str, Any]], dict[str, Any]]:
        """
        Extract the response schema and headers from endpoint data.
        """
        responses = endpoint_data.get("responses", {})
        # Prefer 200, then default, then any other status code
        status_code = None
        if "200" in responses:
            status_code = "200"
        elif "default" in responses:
            status_code = "default"
        else:
            # pick first available
            status_code = next(iter(responses), None)

        if not status_code:
            return None, {}

        response = responses[status_code]
        # The schema is usually under content/application/json/schema
        schema = None
        content = response.get("content", {})
        if "application/json" in content:
            schema = content["application/json"].get("schema")
        elif "application/xml" in content:
            schema = content["application/xml"].get("schema")
        # Fallback: direct schema
        if not schema:
            schema = response.get("schema")

        headers = response.get("headers", {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(
        outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]
    ) -> dict[str, str]:
        """
        Validate and fix output mappings for a step.
        """
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        # Also include headers as potential outputs
        header_paths = {
            f"header:{k.lower()}": f"header:{k.lower()}" for k in headers.keys()}

        fixed_outputs: dict[str, str] = {}
        for out_name, path in outputs.items():
            norm_path = OutputMappingValidator._normalize_property_path(path)
            # Check if path exists in schema or headers
            if norm_path in flat_schema.values() or norm_path in header_paths:
                fixed_outputs[out_name] = norm_path
                continue

            # Try to find best match in schema properties
            best_match = OutputMappingValidator._find_best_property_match(
                out_name, flat_schema)
            if best_match:
                fixed_outputs[out_name] = best_match
                continue

            # Try to find best match in headers
            header_match = OutputMappingValidator._find_best_match(
                out_name.lower(), list(header_paths.keys()))
            if header_match:
                fixed_outputs[out_name] = header_match
                continue

            # If nothing found, keep original
            fixed_outputs[out_name] = norm_path
        return fixed_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        """
        Normalize a property path by stripping leading '$.' and ensuring dot notation.
        """
