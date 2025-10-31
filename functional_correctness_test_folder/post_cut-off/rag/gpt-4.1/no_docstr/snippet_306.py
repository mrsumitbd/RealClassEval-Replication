import re
from typing import Any


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        '''Validate and fix output mappings in a workflow.'''
        steps = workflow.get("steps", [])
        for step in steps:
            outputs = step.get("outputs")
            if not outputs or not isinstance(outputs, dict):
                continue
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            fixed_outputs = OutputMappingValidator._validate_step_outputs(
                outputs, schema, headers)
            step["outputs"] = fixed_outputs
        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        '''Get the endpoint data for a step.'''
        op_id = step.get("operation_id") or step.get("operationId")
        if op_id and op_id in endpoints:
            return endpoints[op_id]
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
        # Prefer 200, then default, then any
        for code in ("200", "default"):
            if code in responses:
                resp = responses[code]
                break
        else:
            resp = next(iter(responses.values()), {})
        schema = {}
        headers = {}
        content = resp.get("content", {})
        if "application/json" in content:
            schema = content["application/json"].get("schema", {})
        elif content:
            # Pick any content type
            schema = next(iter(content.values())).get("schema", {})
        headers = resp.get("headers", {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        '''Validate and fix output mappings for a step.'''
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        header_names = [k for k in headers.keys()]
        fixed_outputs = {}
        for out_name, out_path in outputs.items():
            # Normalize and check if out_path is in schema or headers
            norm_path = OutputMappingValidator._normalize_property_path(
                out_path)
            if norm_path in flat_schema.values():
                fixed_outputs[out_name] = norm_path
                continue
            # Check if it's a header
            if out_path in header_names:
                fixed_outputs[out_name] = out_path
                continue
            # Try to find best property match
            best_match = OutputMappingValidator._find_best_property_match(
                out_name, flat_schema)
            if best_match:
                fixed_outputs[out_name] = best_match
            else:
                # As fallback, keep original
                fixed_outputs[out_name] = out_path
        return fixed_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        '''Normalize a property path by removing array indices.'''
        # Remove [0], [1], etc.
        return re.sub(r"\[\d+\]", "", path)

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        '''Find the best matching string from a list of candidates using sequence matching.'''
        import difflib
        if not candidates:
            return None
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        '''Find the best matching property in the schema for an output name.'''
        candidates = list(flat_schema.keys())
        best = OutputMappingValidator._find_best_match(output_name, candidates)
        if best:
            return flat_schema[best]
        # Try lowercased
        best = OutputMappingValidator._find_best_match(
            output_name.lower(), [c.lower() for c in candidates])
        if best:
            idx = [c.lower() for c in candidates].index(best)
            return list(flat_schema.values())[idx]
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
                # For arrays of objects
                flat.update(OutputMappingValidator._flatten_schema(
                    val["items"]["properties"], path))
        return flat
