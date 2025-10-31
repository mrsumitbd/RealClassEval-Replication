
from typing import Any, Dict, List, Set, Union
import difflib


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''
    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        '''Validate and fix step references in a workflow.
        This function checks all references to steps and their outputs in a workflow
        and fixes any inconsistencies.
        Args:
            workflow: The workflow to validate.
        Returns:
            The validated and fixed workflow.
        '''
        valid_step_ids = set(workflow.get('steps', {}).keys())
        step_outputs = {step_id: step.get(
            'out', []) for step_id, step in workflow.get('steps', {}).items()}

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
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step_id, step in workflow.get('steps', {}).items():
            parameters = step.get('parameters', {})
            for param_name, param_value in parameters.items():
                if isinstance(param_value, str) and param_value.startswith('$steps.'):
                    parts = param_value.split('.')
                    if len(parts) == 3 and parts[1] in valid_step_ids:
                        if parts[2] not in step_outputs[parts[1]]:
                            best_match = ReferenceValidator._find_best_match(
                                parts[2], step_outputs[parts[1]])
                            if best_match:
                                workflow['steps'][step_id]['parameters'][
                                    param_name] = f'$steps.{parts[1]}.{best_match}'

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step_id, step in workflow.get('steps', {}).items():
            if 'requestBody' in step:
                request_body = step['requestBody']
                if isinstance(request_body, str) and request_body.startswith('$steps.'):
                    parts = request_body.split('.')
                    if len(parts) == 3 and parts[1] in valid_step_ids:
                        if parts[2] not in step_outputs[parts[1]]:
                            best_match = ReferenceValidator._find_best_match(
                                parts[2], step_outputs[parts[1]])
                            if best_match:
                                workflow['steps'][step_id][
                                    'requestBody'] = f'$steps.{parts[1]}.{best_match}'
                elif isinstance(request_body, dict):
                    for key, value in request_body.items():
                        if isinstance(value, str) and value.startswith('$steps.'):
                            parts = value.split('.')
                            if len(parts) == 3 and parts[1] in valid_step_ids:
                                if parts[2] not in step_outputs[parts[1]]:
                                    best_match = ReferenceValidator._find_best_match(
                                        parts[2], step_outputs[parts[1]])
                                    if best_match:
                                        workflow['steps'][step_id]['requestBody'][
                                            key] = f'$steps.{parts[1]}.{best_match}'
