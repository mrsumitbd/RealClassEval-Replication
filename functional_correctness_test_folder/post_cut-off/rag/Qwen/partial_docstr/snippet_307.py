
from difflib import get_close_matches
from typing import Any, Dict, List, Set


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
        valid_step_ids = {step['id'] for step in workflow.get('steps', [])}
        step_outputs = {step['id']: step.get(
            'outputs', {}) for step in workflow.get('steps', [])}

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> str | None:
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
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step in workflow.get('steps', []):
            for param, value in step.get('parameters', {}).items():
                if isinstance(value, str) and value.startswith('step:'):
                    step_id, output = value[5:].split('.')
                    if step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            step_id, valid_step_ids)
                        if best_match:
                            step['parameters'][param] = f'step:{best_match}.{output}'
                            print(
                                f'Fixed parameter reference: {value} -> step:{best_match}.{output}')
                    elif output not in step_outputs.get(step_id, {}):
                        best_match = ReferenceValidator._find_best_match(
                            output, step_outputs.get(step_id, {}).keys())
                        if best_match:
                            step['parameters'][param] = f'step:{step_id}.{best_match}'
                            print(
                                f'Fixed parameter reference: {value} -> step:{step_id}.{best_match}')

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step in workflow.get('steps', []):
            request_body = step.get('requestBody', {})
            if isinstance(request_body, dict):
                for key, value in request_body.items():
                    if isinstance(value, str) and value.startswith('step:'):
                        step_id, output = value[5:].split('.')
                        if step_id not in valid_step_ids:
                            best_match = ReferenceValidator._find_best_match(
                                step_id, valid_step_ids)
                            if best_match:
                                request_body[key] = f'step:{best_match}.{output}'
                                print(
                                    f'Fixed request body reference: {value} -> step:{best_match}.{output}')
                        elif output not in step_outputs.get(step_id, {}):
                            best_match = ReferenceValidator._find_best_match(
                                output, step_outputs.get(step_id, {}).keys())
                            if best_match:
                                request_body[key] = f'step:{step_id}.{best_match}'
                                print(
                                    f'Fixed request body reference: {value} -> step:{step_id}.{best_match}')
