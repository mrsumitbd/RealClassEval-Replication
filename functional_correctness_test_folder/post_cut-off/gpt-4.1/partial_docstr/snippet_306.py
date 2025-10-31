
from typing import Any


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        '''Validate and fix output mappings in a workflow.'''
        steps = workflow.get("steps", [])
        for step in steps:
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
        op_id = step.get("operation_id")
        if op_id and op_id in endpoints:
            return endpoints[op_id]
        # Try to match by path and method if operation_id is not present
        path = step.get("path")
        method = step.get("method", "").lower()
        for endpoint in endpoints.values():
            if endpoint.get("path") == path and endpoint.get("method", "").lower() == method:
                return endpoint
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        # Find the 200 or default response
        responses = endpoint_data.get("responses", {})
        response = responses.get("200") or responses.get("default")
        if not response:
            # Try any available response
            for resp in responses.values():
                response = resp
                break
        if not response:
            return {}, {}
        schema = {}
        headers = {}
        content = response.get("content", {})
        if "application/json" in content:
            schema = content["application/json"].get("schema", {})
        elif content:
            # Pick any content type
            schema = next(iter(content.values())).get("schema", {})
        headers = response.get("headers", {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        # Flatten schema and headers
        flat_schema = OutputMappingValidator._flatten_schema(schema.get(
            "properties", {}) if schema.get("type") == "object" else schema, "")
        flat_headers = {k.lower(): k for k in headers.keys()}
        fixed_outputs = {}
        for out_name, out_path in outputs.items():
            norm_path = OutputMappingValidator._normalize_property_path(
                out_path)
            # Check if path is in schema
            if norm_path in flat_schema.values():
                fixed_outputs[out_name] = norm_path
            elif out_name.lower() in flat_headers:
                # Map to header if matches
                fixed_outputs[out_name] = f"headers.{flat_headers[out_name.lower()]}"
            else:
                # Try to find best match in schema
                best = OutputMappingValidator._find_best_property_match(
                    out_name, flat_schema)
                if best:
                    fixed_outputs[out_name] = best
                else:
                    # Keep as is if no match
                    fixed_outputs[out_name] = out_path
        return fixed_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        # Remove leading 'body.' or 'response.' or 'data.' or 'result.' etc.
        for prefix in ("body.", "response.", "data.", "result."):
            if path.startswith(prefix):
                return path[len(prefix):]
        return path

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        # Simple case-insensitive match, then substring, then Levenshtein distance
        target_l = target.lower()
        for cand in candidates:
            if cand.lower() == target_l:
                return cand
        for cand in candidates:
            if target_l in cand.lower() or cand.lower() in target_l:
                return cand
        # Levenshtein distance (simple implementation)

        def levenshtein(a, b):
            if len(a) < len(b):
                return levenshtein(b, a)
            if len(b) == 0:
                return len(a)
            previous_row = range(len(b) + 1)
            for i, c1 in enumerate(a):
                current_row = [i + 1]
                for j, c2 in enumerate(b):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(
                        min(insertions, deletions, substitutions))
                previous_row = current_row
            return previous_row[-1]
        min_dist = float('inf')
        best = None
        for cand in candidates:
            dist = levenshtein(target_l, cand.lower())
            if dist < min_dist:
                min_dist = dist
                best = cand
        if min_dist <= 2:
            return best
        return None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        # Try to match output_name to property names or paths
        candidates = list(flat_schema.keys()) + list(flat_schema.values())
        match = OutputMappingValidator._find_best_match(
            output_name, candidates)
        if match:
            # Return the path
            if match in flat_schema:
                return flat_schema[match]
            else:
                return match
        return None

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.'''
        flat = {}
        if not isinstance(properties, dict):
            return flat
        for prop, val in properties.items():
            path = f"{prefix}.{prop}" if prefix else prop
            if isinstance(val, dict) and val.get("type") == "object" and "properties" in val:
                flat.update(OutputMappingValidator._flatten_schema(
                    val["properties"], path))
            else:
                flat[prop] = path
        return flat
