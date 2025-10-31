
import difflib
from typing import Any


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''
    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        '''Validate and fix step references in a workflow.
        This function checks all references to steps and their outputs in a workflow
        and fixes any inconsistencies.
        Args:
            workflow: The workflow to validate.
        Returns:
            The validated and fixed workflow.
        '''
        valid_step_ids = {step['id'] for step in workflow.get('steps', [])}
        step_outputs = {step['id']: step.get(
            'outputs', {}) for step in workflow.get('steps', [])}

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
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
        for step in workflow.get('steps', []):
            for param in step.get('parameters', {}).values():
                if isinstance(param, str) and param.startswith('${'):
                    ref = param[2:-1]
                    step_id, _, output_key = ref.partition('.')
                    if step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            step_id, list(valid_step_ids))
                        if best_match:
                            param = f'${{{best_match}.{output_key}}}'
                    elif output_key not in step_outputs.get(step_id, {}):
                        best_match = ReferenceValidator._find_best_match(
                            output_key, list(step_outputs.get(step_id, {}).keys()))
                        if best_match:
                            param = f'${{{step_id}.{best_match}}}'

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step in workflow.get('steps', []):
            if 'request_body' in step:
                request_body = step['request_body']
                if isinstance(request_body, str) and request_body.startswith('${'):
                    ref = request_body[2:-1]
                    step_id, _, output_key = ref.partition('.')
                    if step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            step_id, list(valid_step_ids))
                        if best_match:
                            request_body = f'${{{best_match}.{output_key}}}'
                    elif output_key not in step_outputs.get(step_id, {}):
                        best_match = ReferenceValidator._find_best_match(
                            output_key, list(step_outputs.get(step_id, {}).keys()))
                        if best_match:
                            request_body = f'${{{step_id}.{best_match}}}'
