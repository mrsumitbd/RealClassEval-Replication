
from typing import Any, Optional
import difflib


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''
    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        '''Validates and fixes step references in the workflow.
        Args:
            workflow: The workflow to validate and fix.
        Returns:
            The validated and fixed workflow.
        '''
        if not workflow or 'steps' not in workflow:
            return workflow

        valid_step_ids = {step['id']
                          for step in workflow['steps'] if 'id' in step}
        step_outputs = {}
        for step in workflow['steps']:
            if 'id' in step and 'outputs' in step:
                step_outputs[step['id']] = step['outputs']

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> Optional[str]:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates:
            return None
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        if 'parameters' not in workflow:
            return

        for param in workflow['parameters']:
            if 'value' not in param:
                continue
            value = param['value']
            if isinstance(value, str) and value.startswith('${{') and value.endswith('}}'):
                ref = value[3:-2].strip()
                if ref not in valid_step_ids:
                    best_match = ReferenceValidator._find_best_match(
                        ref, list(valid_step_ids))
                    if best_match:
                        param['value'] = f'${{{{{best_match}}}}}'

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step in workflow['steps']:
            if 'request' not in step or 'body' not in step['request']:
                continue
            body = step['request']['body']
            if isinstance(body, str) and body.startswith('${{') and body.endswith('}}'):
                ref = body[3:-2].strip()
                if ref not in valid_step_ids:
                    best_match = ReferenceValidator._find_best_match(
                        ref, list(valid_step_ids))
                    if best_match:
                        step['request']['body'] = f'${{{{{best_match}}}}}'
