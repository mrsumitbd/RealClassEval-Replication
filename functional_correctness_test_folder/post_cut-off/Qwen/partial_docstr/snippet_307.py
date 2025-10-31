
from typing import Any, Dict, List, Set, Optional
from difflib import get_close_matches


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''
    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        valid_step_ids = set(workflow.get('steps', {}).keys())
        step_outputs = {step_id: step.get(
            'output', {}) for step_id, step in workflow.get('steps', {}).items()}

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        matches = get_close_matches(target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        for step in workflow.get('steps', {}).values():
            parameters = step.get('parameters', {})
            for param_name, param_value in parameters.items():
                if isinstance(param_value, str) and param_value.startswith('$'):
                    step_id = param_value[1:]
                    if step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            step_id, list(valid_step_ids))
                        if best_match:
                            parameters[param_name] = f'${best_match}'

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step in workflow.get('steps', {}).values():
            request_body = step.get('requestBody', {})
            for key, value in request_body.items():
                if isinstance(value, str) and value.startswith('$'):
                    step_id = value[1:]
                    if step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            step_id, list(valid_step_ids))
                        if best_match:
                            request_body[key] = f'${best_match}'
