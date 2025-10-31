
from typing import Any, Dict, Set, Optional
from difflib import get_close_matches


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
            if 'parameters' not in step:
                continue
            for param_name, param_value in step['parameters'].items():
                if isinstance(param_value, str) and param_value.startswith('$'):
                    parts = param_value[1:].split('.')
                    if len(parts) >= 2:
                        step_id = parts[0]
                        if step_id not in valid_step_ids:
                            best_match = ReferenceValidator._find_best_match(
                                step_id, list(valid_step_ids))
                            if best_match:
                                new_ref = f'${best_match}.{".".join(parts[1:])}'
                                step['parameters'][param_name] = new_ref

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        for step in workflow.get('steps', []):
            if 'request' not in step or 'body' not in step['request']:
                continue
            body = step['request']['body']
            if isinstance(body, str) and body.startswith('$'):
                parts = body[1:].split('.')
                if len(parts) >= 2:
                    step_id = parts[0]
                    if step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            step_id, list(valid_step_ids))
                        if best_match:
                            new_ref = f'${best_match}.{".".join(parts[1:])}'
                            step['request']['body'] = new_ref
