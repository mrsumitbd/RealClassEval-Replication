
class OutputMappingValidator:

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        validation_results = {}
        for step_name, step in workflow.get('steps', {}).items():
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if endpoint_data:
                schema, headers = OutputMappingValidator._extract_response_info(
                    endpoint_data)
                outputs = step.get('outputs', {})
                validation_results[step_name] = OutputMappingValidator._validate_step_outputs(
                    outputs, schema, headers)
        return validation_results

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        endpoint_name = step.get('endpoint')
        if endpoint_name:
            return endpoints.get(endpoint_name)
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        responses = endpoint_data.get('responses', {})
        schema = {}
        headers = {}
        for response_code, response_data in responses.items():
            if response_code.startswith('2'):
                schema = response_data.get('content', {}).get(
                    'application/json', {}).get('schema', {})
                headers = response_data.get('headers', {})
                break
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        flat_headers = OutputMappingValidator._flatten_schema(headers)
        validation_results = {}
        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if normalized_path.startswith('header.'):
                matched_property = OutputMappingValidator._find_best_property_match(
                    normalized_path[7:], flat_headers)
            else:
                matched_property = OutputMappingValidator._find_best_property_match(
                    normalized_path, flat_schema)
            validation_results[output_name] = matched_property if matched_property else 'Not Found'
        return validation_results

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        return path.replace('[', '.').replace(']', '').replace('"', '')

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        target_parts = target.split('.')
        best_match = None
        best_match_score = 0
        for candidate in candidates:
            candidate_parts = candidate.split('.')
            score = sum(1 for a, b in zip(
                target_parts, candidate_parts) if a == b)
            if score > best_match_score:
                best_match_score = score
                best_match = candidate
        return best_match

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        candidates = list(flat_schema.keys())
        return OutputMappingValidator._find_best_match(output_name, candidates)

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        flat_schema = {}
        for prop_name, prop_data in properties.items():
            current_path = f"{prefix}.{prop_name}" if prefix else prop_name
            if prop_data.get('type') == 'object':
                nested_properties = prop_data.get('properties', {})
                flat_schema.update(OutputMappingValidator._flatten_schema(
                    nested_properties, current_path))
            else:
                flat_schema[current_path] = prop_data.get('type', 'unknown')
        return flat_schema
