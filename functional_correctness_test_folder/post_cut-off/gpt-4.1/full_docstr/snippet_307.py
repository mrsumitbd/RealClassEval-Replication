
from typing import Any
import difflib
import copy
import re


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
        # Deep copy to avoid mutating input
        workflow = copy.deepcopy(workflow)
        steps = workflow.get("steps", [])
        valid_step_ids = set()
        step_outputs = {}

        # Collect valid step ids and their outputs
        for step in steps:
            step_id = step.get("id")
            if step_id:
                valid_step_ids.add(step_id)
                outputs = step.get("outputs", [])
                if isinstance(outputs, dict):
                    step_outputs[step_id] = list(outputs.keys())
                elif isinstance(outputs, list):
                    step_outputs[step_id] = outputs
                else:
                    step_outputs[step_id] = []

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
        steps = workflow.get("steps", [])
        for step in steps:
            parameters = step.get("parameters", {})
            ReferenceValidator._fix_references_in_dict(
                parameters, valid_step_ids, step_outputs)

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        steps = workflow.get("steps", [])
        for step in steps:
            request_body = step.get("requestBody", {})
            ReferenceValidator._fix_references_in_dict(
                request_body, valid_step_ids, step_outputs)

    @staticmethod
    def _fix_references_in_dict(obj: Any, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        # Recursively fix references in dict or list
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    ReferenceValidator._fix_references_in_dict(
                        v, valid_step_ids, step_outputs)
                elif isinstance(v, str):
                    fixed = ReferenceValidator._fix_reference_string(
                        v, valid_step_ids, step_outputs)
                    if fixed != v:
                        obj[k] = fixed
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    ReferenceValidator._fix_references_in_dict(
                        item, valid_step_ids, step_outputs)
                elif isinstance(item, str):
                    fixed = ReferenceValidator._fix_reference_string(
                        item, valid_step_ids, step_outputs)
                    if fixed != item:
                        obj[idx] = fixed

    @staticmethod
    def _fix_reference_string(s: str, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> str:
        # Find all occurrences of {{steps.STEP_ID.outputs.OUTPUT_NAME}}
        pattern = r"\{\{\s*steps\.([^.]+)\.outputs\.([^\}]+)\s*\}\}"

        def repl(match):
            step_id = match.group(1)
            output_name = match.group(2)
            # Fix step_id
            if step_id not in valid_step_ids:
                best_step = ReferenceValidator._find_best_match(
                    step_id, list(valid_step_ids))
                if best_step:
                    step_id_fixed = best_step
                else:
                    step_id_fixed = step_id
            else:
                step_id_fixed = step_id
            # Fix output_name
            outputs = step_outputs.get(step_id_fixed, [])
            if output_name not in outputs:
                best_output = ReferenceValidator._find_best_match(
                    output_name, outputs)
                if best_output:
                    output_name_fixed = best_output
                else:
                    output_name_fixed = output_name
            else:
                output_name_fixed = output_name
            return f"{{{{steps.{step_id_fixed}.outputs.{output_name_fixed}}}}}"
        return re.sub(pattern, repl, s)
