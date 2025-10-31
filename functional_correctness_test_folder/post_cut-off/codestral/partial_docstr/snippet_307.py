
import difflib
from typing import Any


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        valid_step_ids = set(workflow.keys())
        step_outputs = {step_id: step.get('outputs', {})
                        for step_id, step in workflow.items()}

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
        for step_id, step in workflow.items():
            if 'parameters' in step:
                for param_name, param_value in step['parameters'].items():
                    if isinstance(param_value, str) and param_value.startswith('${'):
                        ref_step_id = param_value[2:-1].split('.')[0]
                        if ref_step_id not in valid_step_ids:
                            best_match = ReferenceValidator._find_best_match(
                                ref_step_id, list(valid_step_ids))
                            if best_match:
                                step['parameters'][
                                    param_name] = f'${{{best_match}.{param_value[2:-1].split(".")[1]}}}'

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step_id, step in workflow.items():
            if 'request' in step and 'body' in step['request']:
                body = step['request']['body']
                if isinstance(body, str) and body.startswith('${'):
                    ref_step_id = body[2:-1].split('.')[0]
                    if ref_step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            ref_step_id, list(valid_step_ids))
                        if best_match:
                            step['request']['body'] = f'${{{best_match}.{body[2:-1].split(".")[1]}}}'
