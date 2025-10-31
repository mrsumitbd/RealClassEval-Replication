
from typing import Any, Optional


class OutputMappingValidator:

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        errors = {}
        for step_name, step_data in workflow.get('steps', {}).items():
            if 'outputs' not in step_data:
                continue
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step_data, endpoints)
            if not endpoint_data:
                errors[step_name] = "Endpoint not found"
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            validation_errors = OutputMappingValidator._validate_step_outputs(
                step_data['outputs'], schema, headers)
            if validation_errors:
                errors[step_name] = validation_errors
        return errors

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> Optional[dict[str, Any]]:
        endpoint_key = step.get('endpoint')
        if not endpoint_key:
            return None
        return endpoints.get(endpoint_key)

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        responses = endpoint_data.get('responses', {})
        success_response = responses.get('200', {}) or responses.get('201', {})
        schema = success_response.get('content', {}).get(
            'application/json', {}).get('schema', {})
        headers = success_response.get('headers', {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        errors = {}
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        for output_name, output_path in outputs.items():
            if output_path.startswith('$header.'):
                header_name = output_path[8:]
                if header_name not in headers:
                    errors[output_name] = f"Header '{header_name}' not found"
            else:
                normalized_path = OutputMappingValidator._normalize_property_path(
                    output_path)
                if normalized_path not in flat_schema:
                    best_match = OutputMappingValidator._find_best_property_match(
                        output_name, flat_schema)
                    if best_match:
                        errors[output_name] = f"Path '{output_path}' not found. Did you mean '{best_match}'?"
                    else:
                        errors[output_name] = f"Path '{output_path}' not found"
        return errors

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        return path.replace('$.', '').replace('.[', '[')

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> Optional[str]:
        from difflib import get_close_matches
        matches = get_close_matches(target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> Optional[str]:
        candidates = list(flat_schema.keys())
        return OutputMappingValidator._find_best_match(output_name, candidates)

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        flat = {}
        for prop_name, prop_data in properties.items():
            current_path = f"{prefix}.{prop_name}" if prefix else prop_name
            if 'properties' in prop_data:
                flat.update(OutputMappingValidator._flatten_schema(
                    prop_data['properties'], current_path))
            elif 'items' in prop_data and 'properties' in prop_data['items']:
                flat.update(OutputMappingValidator._flatten_schema(
                    prop_data['items']['properties'], f"{current_path}[0]"))
            else:
                flat[current_path] = prop_data.get('type', 'unknown')
        return flat
