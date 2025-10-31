import re
from typing import Any
from difflib import SequenceMatcher


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
        steps = workflow.get("steps", [])
        for step in steps:
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            outputs = step.get("outputs", {})
            if outputs:
                fixed_outputs = OutputMappingValidator._validate_step_outputs(
                    outputs, schema, headers)
                step["outputs"] = fixed_outputs
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
        op_id = step.get("operation_id") or step.get("operationId")
        if op_id and op_id in endpoints:
            return endpoints[op_id]
        # Try to match by path and method if operation_id is not present
        path = step.get("path")
        method = step.get("method")
        if path and method:
            for ep in endpoints.values():
                if ep.get("path") == path and ep.get("method", "").lower() == method.lower():
                    return ep
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        '''
        responses = endpoint_data.get("responses", {})
        # Prefer 200, then default, then any
        for code in ("200", "default"):
            if code in responses:
                resp = responses[code]
                break
        else:
            # Pick the first available response
            resp = next(iter(responses.values()), {})
        schema = {}
        headers = {}
        content = resp.get("content", {})
        if "application/json" in content:
            schema = content["application/json"].get("schema", {})
        elif content:
            # Pick any content type
            schema = next(iter(content.values())).get("schema", {})
        if "headers" in resp:
            headers = resp["headers"]
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
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        header_names = set(headers.keys())
        fixed_outputs = {}
        for out_name, out_path in outputs.items():
            norm_path = OutputMappingValidator._normalize_property_path(
                out_path)
            # Check if path is in schema or headers
            if norm_path in flat_schema.values():
                fixed_outputs[out_name] = norm_path
            elif out_path in header_names:
                fixed_outputs[out_name] = out_path
            else:
                # Try to find best match in schema
                best_match = OutputMappingValidator._find_best_property_match(
                    out_name, flat_schema)
                if best_match:
                    fixed_outputs[out_name] = best_match
                else:
                    # Try to find best match in headers
                    best_header = OutputMappingValidator._find_best_match(
                        out_name, list(header_names))
                    if best_header:
                        fixed_outputs[out_name] = best_header
                    else:
                        # Fallback to original
                        fixed_outputs[out_name] = out_path
        return fixed_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        '''Normalize a property path by removing array indices.
        Args:
            path: The property path to normalize.
        Returns:
            The normalized property path.
        '''
        # Remove [0], [1], etc. from paths like "foo[0].bar"
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
        if not candidates:
            return None
        best = None
        best_ratio = 0.0
        for cand in candidates:
            ratio = SequenceMatcher(None, target.lower(), cand.lower()).ratio()
            if ratio > best_ratio:
                best = cand
                best_ratio = ratio
        return best if best_ratio > 0.5 else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        '''Find the best matching property in the schema for an output name.
        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.
        Returns:
            The path to the matching property, or None if no match is found.
        '''
        candidates = list(flat_schema.keys())
        best = OutputMappingValidator._find_best_match(output_name, candidates)
        if best:
            return flat_schema[best]
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
        for prop, val in properties.items():
            path = f"{prefix}.{prop}" if prefix else prop
            flat[prop] = path
            if val.get("type") == "object" and "properties" in val:
                flat.update(OutputMappingValidator._flatten_schema(
                    val["properties"], path))
            elif val.get("type") == "array" and "items" in val and "properties" in val["items"]:
                # For arrays of objects, flatten the items' properties
                flat.update(OutputMappingValidator._flatten_schema(
                    val["items"]["properties"], path))
        return flat
