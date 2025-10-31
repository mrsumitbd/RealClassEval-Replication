
from typing import Any


class OutputMappingValidator:

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        results = {}
        steps = workflow.get("steps", [])
        for step in steps:
            step_name = step.get("name")
            outputs = step.get("outputs", {})
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                results[step_name] = {"error": "Endpoint not found"}
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            output_results = OutputMappingValidator._validate_step_outputs(
                outputs, schema, headers)
            results[step_name] = output_results
        return results

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        endpoint_name = step.get("endpoint")
        if not endpoint_name:
            return None
        return endpoints.get(endpoint_name)

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        responses = endpoint_data.get("responses", {})
        # Prefer 200, then default, then any
        for code in ("200", "default"):
            if code in responses:
                response = responses[code]
                break
        else:
            if responses:
                response = next(iter(responses.values()))
            else:
                return {}, {}
        schema = response.get("content", {}).get(
            "application/json", {}).get("schema", {})
        headers = response.get("headers", {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        header_names = [h.lower() for h in headers.keys()]
        results = {}
        for output_name, output_path in outputs.items():
            norm_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if norm_path in flat_schema:
                results[output_name] = "ok"
            elif norm_path.lower() in header_names:
                results[output_name] = "ok (header)"
            else:
                best = OutputMappingValidator._find_best_property_match(
                    norm_path, flat_schema)
                if not best:
                    best = OutputMappingValidator._find_best_match(
                        norm_path, header_names)
                    if best:
                        results[output_name] = f"not found, did you mean header '{best}'?"
                    else:
                        results[output_name] = "not found"
                else:
                    results[output_name] = f"not found, did you mean '{best}'?"
        return results

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        return path.replace("[", ".").replace("]", "").replace("..", ".").strip(".")

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        import difflib
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        return OutputMappingValidator._find_best_match(output_name, list(flat_schema.keys()))

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        flat = {}
        for prop, prop_schema in properties.items():
            path = f"{prefix}.{prop}" if prefix else prop
            if prop_schema.get("type") == "object" and "properties" in prop_schema:
                flat.update(OutputMappingValidator._flatten_schema(
                    prop_schema["properties"], path))
            else:
                flat[path] = prop_schema.get("type", "unknown")
        return flat
