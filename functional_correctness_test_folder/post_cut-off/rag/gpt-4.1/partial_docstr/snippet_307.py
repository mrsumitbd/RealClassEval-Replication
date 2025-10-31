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
        if not workflow or "steps" not in workflow:
            return workflow

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
            if not isinstance(parameters, dict):
                continue
            for param_key, param_value in parameters.items():
                if isinstance(param_value, str):
                    # Look for references like {{steps.step_id.outputs.output_name}}
                    fixed_value = ReferenceValidator._fix_reference_string(
                        param_value, valid_step_ids, step_outputs)
                    if fixed_value != param_value:
                        parameters[param_key] = fixed_value
                elif isinstance(param_value, list):
                    for idx, v in enumerate(param_value):
                        if isinstance(v, str):
                            fixed_value = ReferenceValidator._fix_reference_string(
                                v, valid_step_ids, step_outputs)
                            if fixed_value != v:
                                param_value[idx] = fixed_value
                elif isinstance(param_value, dict):
                    for k, v in param_value.items():
                        if isinstance(v, str):
                            fixed_value = ReferenceValidator._fix_reference_string(
                                v, valid_step_ids, step_outputs)
                            if fixed_value != v:
                                param_value[k] = fixed_value

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
            if not isinstance(request_body, dict):
                continue
            for k, v in request_body.items():
                if isinstance(v, str):
                    fixed_value = ReferenceValidator._fix_reference_string(
                        v, valid_step_ids, step_outputs)
                    if fixed_value != v:
                        request_body[k] = fixed_value
                elif isinstance(v, list):
                    for idx, item in enumerate(v):
                        if isinstance(item, str):
                            fixed_value = ReferenceValidator._fix_reference_string(
                                item, valid_step_ids, step_outputs)
                            if fixed_value != item:
                                v[idx] = fixed_value
                elif isinstance(v, dict):
                    for subk, subv in v.items():
                        if isinstance(subv, str):
                            fixed_value = ReferenceValidator._fix_reference_string(
                                subv, valid_step_ids, step_outputs)
                            if fixed_value != subv:
                                v[subk] = fixed_value

    @staticmethod
    def _fix_reference_string(value: str, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> str:
        # Only fix references of the form {{steps.step_id.outputs.output_name}}
        import re
        pattern = r"\{\{\s*steps\.([^.]+)\.outputs\.([^\}]+)\s*\}\}"

        def repl(match):
            step_id, output_name = match.group(1), match.group(2)
            fixed_step_id = step_id if step_id in valid_step_ids else ReferenceValidator._find_best_match(
                step_id, list(valid_step_ids))
            if not fixed_step_id:
                return match.group(0)
            outputs = step_outputs.get(fixed_step_id, [])
            fixed_output_name = output_name if output_name in outputs else ReferenceValidator._find_best_match(
                output_name, outputs)
            if not fixed_output_name:
                return "{{steps.%s.outputs.%s}}" % (fixed_step_id, output_name)
            return "{{steps.%s.outputs.%s}}" % (fixed_step_id, fixed_output_name)
        return re.sub(pattern, repl, value)
