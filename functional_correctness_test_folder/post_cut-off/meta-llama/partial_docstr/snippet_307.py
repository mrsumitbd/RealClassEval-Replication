
from typing import Any, Dict, List, Set, Union
import difflib


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''
    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        valid_step_ids = set(workflow.get('steps', {}).keys())
        step_outputs = {step_id: step.get(
            'out') for step_id, step in workflow.get('steps', {}).items()}

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Union[str, None]:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates:
            return None
        best_match = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return best_match[0] if best_match else None

    @staticmethod
    def _fix_parameter_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        for step_id, step in workflow.get('steps', {}).items():
            parameters = step.get('parameters', {})
            for param_name, param_value in parameters.items():
                if isinstance(param_value, str) and param_value.startswith('$steps.'):
                    parts = param_value.split('.')
                    if len(parts) == 3 and parts[1] in valid_step_ids:
                        continue
                    else:
                        best_match = ReferenceValidator._find_best_match(
                            parts[1], list(valid_step_ids))
                        if best_match:
                            workflow['steps'][step_id]['parameters'][
                                param_name] = f'$steps.{best_match}.{parts[-1]}'

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step_id, step in workflow.get('steps', {}).items():
            request_body = step.get('requestBody')
            if isinstance(request_body, dict):
                for key, value in request_body.items():
                    if isinstance(value, str) and value.startswith('$steps.'):
                        parts = value.split('.')
                        if len(parts) == 3 and parts[1] in valid_step_ids:
                            continue
                        else:
                            best_match = ReferenceValidator._find_best_match(
                                parts[1], list(valid_step_ids))
                            if best_match:
                                workflow['steps'][step_id]['requestBody'][
                                    key] = f'$steps.{best_match}.{parts[-1]}'
                    elif isinstance(value, dict):
                        ReferenceValidator._fix_dict_references(
                            value, valid_step_ids)

    @staticmethod
    def _fix_dict_references(data: Dict[str, Any], valid_step_ids: Set[str]) -> None:
        for key, value in data.items():
            if isinstance(value, str) and value.startswith('$steps.'):
                parts = value.split('.')
                if len(parts) == 3 and parts[1] in valid_step_ids:
                    continue
                else:
                    best_match = ReferenceValidator._find_best_match(
                        parts[1], list(valid_step_ids))
                    if best_match:
                        data[key] = f'$steps.{best_match}.{parts[-1]}'
            elif isinstance(value, dict):
                ReferenceValidator._fix_dict_references(value, valid_step_ids)
