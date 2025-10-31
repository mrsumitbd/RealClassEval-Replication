
from typing import Any, Dict, List, Set
import difflib


class ReferenceValidator:
    """Validates and fixes step references in Arazzo workflows."""

    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix step references in a workflow.

        This function checks all references to steps and their outputs in a workflow
        and fixes any inconsistencies.

        Args:
            workflow: The workflow to validate.

        Returns:
            The validated and fixed workflow.
        """
        valid_step_ids = set(workflow.get('steps', {}).keys())
        step_outputs = {step_id: step.get(
            'outputs', {}) for step_id, step in workflow.get('steps', {}).items()}

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> str | None:
        """Find the best matching string from a list of candidates using sequence matching.

        Args:
            target: The target string to match.
            candidates: List of candidate strings.

        Returns:
            The best matching string or None if candidates is empty.
        """
        if not candidates:
            return None
        return difflib.get_close_matches(target, candidates, n=1, cutoff=0.6)[0]

    @staticmethod
    def _fix_parameter_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        """Fix parameter references in a workflow.

        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        for step_id, step in workflow.get('steps', {}).items():
            for param, value in step.get('inputs', {}).items():
                if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                    reference = value[2:-2].strip()
                    parts = reference.split('.')
                    if len(parts) == 2 and parts[0] in valid_step_ids and parts[1] in step_outputs.get(parts[0], {}):
                        continue
                    elif len(parts) == 1 and parts[0] in valid_step_ids:
                        continue
                    else:
                        best_match_step = ReferenceValidator._find_best_match(
                            parts[0], list(valid_step_ids))
                        if best_match_step:
                            if len(parts) == 2:
                                workflow['steps'][step_id]['inputs'][param] = '{{ ' + \
                                    best_match_step + '.' + parts[1] + ' }}'
                            else:
                                workflow['steps'][step_id]['inputs'][param] = '{{ ' + \
                                    best_match_step + ' }}'

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        """Fix request body references in a workflow.

        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        for step_id, step in workflow.get('steps', {}).items():
            if 'requestBody' in step:
                request_body = step['requestBody']
                if isinstance(request_body, str) and request_body.startswith('{{') and request_body.endswith('}}'):
                    reference = request_body[2:-2].strip()
                    parts = reference.split('.')
                    if len(parts) == 2 and parts[0] in valid_step_ids and parts[1] in step_outputs.get(parts[0], {}):
                        continue
                    elif len(parts) == 1 and parts[0] in valid_step_ids:
                        continue
                    else:
                        best_match_step = ReferenceValidator._find_best_match(
                            parts[0], list(valid_step_ids))
                        if best_match_step:
                            if len(parts) == 2:
                                workflow['steps'][step_id]['requestBody'] = '{{ ' + \
                                    best_match_step + '.' + parts[1] + ' }}'
                            else:
                                workflow['steps'][step_id]['requestBody'] = '{{ ' + \
                                    best_match_step + ' }}'
                elif isinstance(request_body, dict):
                    for key, value in request_body.items():
                        if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                            reference = value[2:-2].strip()
                            parts = reference.split('.')
                            if len(parts) == 2 and parts[0] in valid_step_ids and parts[1] in step_outputs.get(parts[0], {}):
                                continue
                            elif len(parts) == 1 and parts[0] in valid_step_ids:
                                continue
                            else:
                                best_match_step = ReferenceValidator._find_best_match(
                                    parts[0], list(valid_step_ids))
                                if best_match_step:
                                    if len(parts) == 2:
                                        workflow['steps'][step_id]['requestBody'][
                                            key] = '{{ ' + best_match_step + '.' + parts[1] + ' }}'
                                    else:
                                        workflow['steps'][step_id]['requestBody'][
                                            key] = '{{ ' + best_match_step + ' }}'
