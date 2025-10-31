
import difflib
import re
from typing import Any, Dict, List, Set, Union


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
        steps = workflow.get('steps', {})
        valid_step_ids: Set[str] = set(steps.keys())
        # Build a mapping of step outputs (assumed to be a dict of output names)
        step_outputs: Dict[str, Any] = {
            step_id: step.get('outputs', {}) for step_id, step in steps.items()
        }

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
        if not candidates:
            return None
        best_candidate = None
        best_ratio = 0.0
        for candidate in candidates:
            ratio = difflib.SequenceMatcher(None, target, candidate).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_candidate = candidate
        # Accept only if similarity is reasonably high
        return best_candidate if best_ratio >= 0.6 else None

    @staticmethod
    def _parse_reference(ref: str) -> tuple[str, str] | None:
        '''Parse a reference string of the form "step_id.output_name".'''
        if '.' not in ref:
            return None
        step_id, output_name = ref.split('.', 1)
        return step_id, output_name

    @staticmethod
    def _replace_reference(original: str, new_step_id: str) -> str:
        '''Replace the step part of a reference with a new step id.'''
        parts = original.split('.', 1)
        if len(parts) != 2:
            return original
        return f'{new_step_id}.{parts[1]}'

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        steps = workflow.get('steps', {})
        for step_id, step in steps.items():
            params = step.get('parameters', {})
            for key, value in list(params.items()):
                if isinstance(value, str):
                    parsed = ReferenceValidator._parse_reference(value)
                    if parsed:
                        ref_step, ref_output = parsed
                        # Validate step id
                        if ref_step not in valid_step_ids:
                            best = ReferenceValidator._find_best_match(
                                ref_step, list(valid_step_ids))
                            if best:
                                ref_step = best
                                value = ReferenceValidator._replace_reference(
                                    value, ref_step)
                        # Validate output name
                        if ref_step in step_outputs and ref_output not in step_outputs[ref_step]:
                            # If output not found, set to None
                            value = None
                        params[key] = value
                elif isinstance(value, dict) or isinstance(value, list):
                    # Recursively handle nested structures
                    ReferenceValidator._fix_parameter_references_in_structure(
                        value, valid_step_ids, step_outputs
                    )
            step['parameters'] = params

    @staticmethod
    def _fix_parameter_references_in_structure(
        obj: Union[Dict[str, Any], List[Any]],
        valid_step_ids: Set[str],
        step_outputs: Dict[str, Any]
    ) -> None:
        '''Recursively fix references inside a dict or list.'''
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if isinstance(v, str):
                    parsed = ReferenceValidator._parse_reference(v)
                    if parsed:
                        ref_step, ref_output = parsed
                        if ref_step not in valid_step_ids:
                            best = ReferenceValidator._find_best_match(
                                ref_step, list(valid_step_ids))
                            if best:
                                ref_step = best
                                v = ReferenceValidator._replace_reference(
                                    v, ref_step)
                        if ref_step in step_outputs and ref_output not in step_outputs[ref_step]:
                            v = None
                        obj[k] = v
                elif isinstance(v, dict) or isinstance(v, list):
                    ReferenceValidator._fix_parameter_references_in_structure(
                        v, valid_step_ids, step_outputs)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                if isinstance(item, str):
                    parsed = ReferenceValidator._parse_reference(item)
                    if parsed:
                        ref_step, ref_output = parsed
                        if ref_step not in valid_step_ids:
                            best = ReferenceValidator._find_best_match(
                                ref_step, list(valid_step_ids))
                            if best:
                                ref_step = best
                                item = ReferenceValidator._replace_reference(
                                    item, ref_step)
                        if ref_step in step_outputs and ref_output not in step_outputs[ref_step]:
                            item = None
                        obj[idx] = item
                elif isinstance(item, dict) or isinstance(item, list):
                    ReferenceValidator._fix_parameter_references_in_structure(
                        item, valid_step_ids, step_outputs)

    @staticmethod
    def _fix_request_body_references(workflow: dict[str
