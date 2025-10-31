
from typing import Any, Dict, List, Optional, Tuple


class OutputMappingValidator:

    @staticmethod
    def validate_output_mappings(workflow: Dict[str, Any], openapi_spec: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        results = {}
        for step_name, step in workflow.get('steps', {}).items():
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                results[step_name] = {'error': 'Endpoint not found'}
                continue

            response_schema, response_headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            outputs = step.get('outputs', {})
            validated_outputs = OutputMappingValidator._validate_step_outputs(
                outputs, response_schema, response_headers)
            results[step_name] = validated_outputs
        return results

    @staticmethod
    def _get_endpoint_for_step(step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        endpoint_id = step.get('endpoint_id')
        return endpoints.get(endpoint_id)

    @staticmethod
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        response_data = endpoint_data.get('responses', {}).get('200', {})
        schema = response_data.get('content', {}).get(
            'application/json', {}).get('schema', {})
        headers = response_data.get('headers', {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: Dict[str, str], schema: Dict[str, Any], headers: Dict[str, Any]) -> Dict[str, str]:
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        flat_headers = {k.lower(): v for k, v in headers.items()}
        validated_outputs = {}
        for output_name, target in outputs.items():
            if target.lower() in flat_headers:
                validated_outputs[output_name] = target
            else:
                best_match = OutputMappingValidator._find_best_property_match(
                    output_name, flat_schema)
                if best_match:
                    validated_outputs[output_name] = best_match
                else:
                    validated_outputs[output_name] = 'No match found'
        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        return path.replace('.', '/').strip('/').lower()

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        target = OutputMappingValidator._normalize_property_path(target)
        for candidate in candidates:
            if OutputMappingValidator._normalize_property_path(candidate) == target:
                return candidate
        return None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> Optional[str]:
        candidates = list(flat_schema.keys())
        return OutputMappingValidator._find_best_match(output_name, candidates)

    @staticmethod
    def _flatten_schema(properties: Dict[str, Any], prefix: str = '') -> Dict[str, str]:
        flat = {}
        for key, value in properties.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if 'properties' in value:
                flat.update(OutputMappingValidator._flatten_schema(
                    value['properties'], new_key))
            else:
                flat[new_key] = value.get('type', 'unknown')
        return flat
