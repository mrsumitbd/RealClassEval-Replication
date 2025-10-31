
import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Set


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
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates:
            return None

        best_match = None
        best_ratio = 0.0

        for candidate in candidates:
            ratio = SequenceMatcher(None, target, candidate).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = candidate

        return best_match if best_ratio > 0.6 else None

    @staticmethod
    def _fix_parameter_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        pattern = re.compile(r'\$\{steps\.([^\.]+)\.outputs\.([^\}]+)\}')

        for step in workflow.get('steps', []):
            for param in step.get('parameters', {}).values():
                if isinstance(param, str):
                    matches = pattern.findall(param)
                    for step_id, output_key in matches:
                        if step_id not in valid_step_ids:
                            best_match = ReferenceValidator._find_best_match(
                                step_id, list(valid_step_ids))
                            if best_match:
                                param = param.replace(
                                    f'${{steps.{step_id}.outputs.{output_key}}}', f'${{steps.{best_match}.outputs.{output_key}}}')
                        elif output_key not in step_outputs.get(step_id, {}):
                            best_match = ReferenceValidator._find_best_match(
                                output_key, list(step_outputs.get(step_id, {}).keys()))
                            if best_match:
                                param = param.replace(
                                    f'${{steps.{step_id}.outputs.{output_key}}}', f'${{steps.{step_id}.outputs.{best_match}}}')

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        pattern = re.compile(r'\$\{steps\.([^\.]+)\.outputs\.([^\}]+)\}')

        for step in workflow.get('steps', []):
            if 'request_body' in step:
                request_body = step['request_body']
                if isinstance(request_body, str):
                    matches = pattern.findall(request_body)
                    for step_id, output_key in matches:
                        if step_id not in valid_step_ids:
                            best_match = ReferenceValidator._find_best_match(
                                step_id, list(valid_step_ids))
                            if best_match:
                                request_body = request_body.replace(
                                    f'${{steps.{step_id}.outputs.{output_key}}}', f'${{steps.{best_match}.outputs.{output_key}}}')
                        elif output_key not in step_outputs.get(step_id, {}):
                            best_match = ReferenceValidator._find_best_match(
                                output_key, list(step_outputs.get(step_id, {}).keys()))
                            if best_match:
                                request_body = request_body.replace(
                                    f'${{steps.{step_id}.outputs.{output_key}}}', f'${{steps.{step_id}.outputs.{best_match}}}')
