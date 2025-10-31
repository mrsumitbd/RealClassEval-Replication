
from typing import Any
import difflib
import re


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        '''Validate and fix output mappings in a workflow.'''
        if "steps" not in workflow or not isinstance(workflow["steps"], list):
            return workflow

        for step in workflow["steps"]:
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            outputs = step.get("outputs", {})
            fixed_outputs = OutputMappingValidator._validate_step_outputs(
                outputs, schema, headers)
            step["outputs"] = fixed_outputs
        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        '''Get the endpoint data for a step.'''
        operation_id = step.get("operation_id")
        if operation_id and operation_id in endpoints:
            return endpoints[operation_id]
        # Try to match by path and method if available
        path = step.get("path")
        method = step.get("method")
        if path and method:
            for ep in endpoints.values():
                if ep.get("path") == path and ep.get("method", "").lower() == method.lower():
                    return ep
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.'''
        responses = endpoint_data.get("responses", {})
        # Prefer 200, then 201, then default, then any
        for code in ("200", "201", "default"):
            if code in responses:
                resp = responses[code]
                schema = resp.get("schema", {})
                headers = resp.get("headers", {})
                return schema, headers
        # Fallback: pick any response
        for resp in responses.values():
            schema = resp.get("schema", {})
            headers = resp.get("headers", {})
            return schema, headers
        return {}, {}

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        '''Validate and fix output mappings for a step.'''
        # Flatten schema and headers
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        flat_headers = {k: f"headers.{k}" for k in headers.keys()}
        all_flat = {**flat_schema, **flat_headers}

        fixed_outputs = {}
        for out_name, out_path in outputs.items():
            norm_path = OutputMappingValidator._normalize_property_path(
                out_path)
            # Check if normalized path is in schema or headers
            if norm_path in all_flat.values():
                fixed_outputs[out_name] = norm_path
            else:
                # Try to find best match for output name in schema/headers
                best_match = OutputMappingValidator._find_best_property_match(
                    out_name, all_flat)
                if best_match:
                    fixed_outputs[out_name] = best_match
                else:
                    # Fallback: keep original
                    fixed_outputs[out_name] = out_path
        return fixed_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        '''Normalize a property path by removing array indices.'''
        # Remove [0], [1], etc.
        return re.sub(r'\[\d+\]', '', path)

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        '''Find the best matching string from a list of candidates using sequence matching.'''
        if not candidates:
            return None
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        '''Find the best matching property in the schema for an output name.'''
        # Try exact match on property name
        for prop, path in flat_schema.items():
            if output_name.lower() == prop.lower():
                return path
        # Try close match
        best = OutputMappingValidator._find_best_match(
            output_name, list(flat_schema.keys()))
        if best:
            return flat_schema[best]
        return None

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.'''
        flat = {}
        for prop, val in properties.items():
            path = f"{prefix}.{prop}" if prefix else prop
            flat[prop] = path
            if val.get("type") == "object" and "properties" in val:
                flat.update(OutputMappingValidator._flatten_schema(
                    val["properties"], path))
            elif val.get("type") == "array" and "items" in val and "properties" in val["items"]:
                # For arrays, flatten the items' properties
                flat.update(OutputMappingValidator._flatten_schema(
                    val["items"]["properties"], path))
        return flat
