
import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(workflow: Dict[str, Any], openapi_spec: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        '''Validate and fix output mappings in a workflow.'''
        for step in workflow.get('steps', []):
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if endpoint_data:
                response_schema, response_headers = OutputMappingValidator._extract_response_info(
                    endpoint_data)
                if 'outputs' in step:
                    step['outputs'] = OutputMappingValidator._validate_step_outputs(
                        step['outputs'], response_schema, response_headers)
        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        '''Get the endpoint data for a step.'''
        if 'endpoint' in step:
            endpoint_name = step['endpoint']
            if endpoint_name in endpoints:
                return endpoints[endpoint_name]
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        '''Extract response schema and headers from endpoint data.'''
        response_schema = endpoint_data.get('responses', {}).get('200', {}).get(
            'content', {}).get('application/json', {}).get('schema', {})
        response_headers = endpoint_data.get(
            'responses', {}).get('200', {}).get('headers', {})
        return response_schema, response_headers

    @staticmethod
    def _validate_step_outputs(outputs: Dict[str, str], schema: Dict[str, Any], headers: Dict[str, Any]) -> Dict[str, str]:
        '''Validate and fix output mappings for a step.'''
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        validated_outputs = {}
        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if normalized_path in flat_schema:
                validated_outputs[output_name] = normalized_path
            else:
                best_match = OutputMappingValidator._find_best_property_match(
                    output_name, flat_schema)
                if best_match:
                    validated_outputs[output_name] = best_match
        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        '''Normalize a property path by removing array indices.'''
        return re.sub(r'\[\d+\]', '', path)

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        '''Find the best matching string from a list of candidates using sequence matching.'''
        if not candidates:
            return None
        best_match = max(candidates, key=lambda candidate: SequenceMatcher(
            None, target, candidate).ratio())
        return best_match

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> Optional[str]:
        '''Find the best matching property in the schema for an output name.'''
        candidates = list(flat_schema.keys())
        best_match = OutputMappingValidator._find_best_match(
            output_name, candidates)
        return flat_schema.get(best_match) if best_match else None

    @staticmethod
    def _flatten_schema(properties: Dict[str, Any], prefix: str = '') -> Dict[str, str]:
        '''Flatten a nested schema into a dictionary of property paths.'''
        flat_schema = {}
        for prop_name, prop_data in properties.items():
            prop_path = f"{prefix}.{prop_name}" if prefix else prop_name
            if 'properties' in prop_data:
                flat_schema.update(OutputMappingValidator._flatten_schema(
                    prop_data['properties'], prop_path))
            else:
                flat_schema[prop_name] = prop_path
        return flat_schema
