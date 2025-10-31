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
                    # Look for references like {{steps.step_id.output}}
                    fixed_value = ReferenceValidator._fix_reference_string(
                        param_value, valid_step_ids, step_outputs)
                    if fixed_value != param_value:
                        parameters[param_key] = fixed_value
                elif isinstance(param_value, list):
                    for idx, item in enumerate(param_value):
                        if isinstance(item, str):
                            fixed_item = ReferenceValidator._fix_reference_string(
                                item, valid_step_ids, step_outputs)
                            if fixed_item != item:
                                param_value[idx] = fixed_item
                elif isinstance(param_value, dict):
                    for k, v in param_value.items():
                        if isinstance(v, str):
                            fixed_v = ReferenceValidator._fix_reference_string(
                                v, valid_step_ids, step_outputs)
                            if fixed_v != v:
                                param_value[k] = fixed_v

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
            request_body = step.get("requestBody")
            if isinstance(request_body, dict):
                ReferenceValidator._fix_dict_references(
                    request_body, valid_step_ids, step_outputs)
            elif isinstance(request_body, str):
                fixed = ReferenceValidator._fix_reference_string(
                    request_body, valid_step_ids, step_outputs)
                if fixed != request_body:
                    step["requestBody"] = fixed

    @staticmethod
    def _fix_reference_string(value: str, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> str:
        # Looks for patterns like {{steps.step_id.output}}
        import re
        pattern = r"\{\{\s*steps\.([a-zA-Z0-9_\-]+)\.([a-zA-Z0-9_\-]+)\s*\}\}"

        def repl(match):
            step_id, output = match.group(1), match.group(2)
            fixed_step_id = step_id if step_id in valid_step_ids else ReferenceValidator._find_best_match(
                step_id, list(valid_step_ids))
            if not fixed_step_id:
                return match.group(0)
            outputs = step_outputs.get(fixed_step_id, [])
            fixed_output = output if output in outputs else ReferenceValidator._find_best_match(
                output, outputs)
            if not fixed_output:
                return match.group(0)
            return "{{steps.%s.%s}}" % (fixed_step_id, fixed_output)
        return re.sub(pattern, repl, value)

    @staticmethod
    def _fix_dict_references(obj: Any, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str):
                    fixed = ReferenceValidator._fix_reference_string(
                        v, valid_step_ids, step_outputs)
                    if fixed != v:
                        obj[k] = fixed
                elif isinstance(v, dict) or isinstance(v, list):
                    ReferenceValidator._fix_dict_references(
                        v, valid_step_ids, step_outputs)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                if isinstance(item, str):
                    fixed = ReferenceValidator._fix_reference_string(
                        item, valid_step_ids, step_outputs)
                    if fixed != item:
                        obj[idx] = fixed
                elif isinstance(item, dict) or isinstance(item, list):
                    ReferenceValidator._fix_dict_references(
                        item, valid_step_ids, step_outputs)
