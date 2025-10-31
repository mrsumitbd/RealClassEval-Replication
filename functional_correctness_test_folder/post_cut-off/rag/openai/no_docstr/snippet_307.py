
import difflib
from typing import Any, Dict, List, Set, Union


class ReferenceValidator:
    """Validates and fixes step references in Arazzo workflows."""

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        """
        Validate and fix step references in a workflow.
        This function checks all references to steps and their outputs in a workflow
        and fixes any inconsistencies.
        Args:
            workflow: The workflow to validate.
        Returns:
            The validated and fixed workflow.
        """
        # Collect step ids and outputs
        steps = workflow.get("steps", [])
        valid_step_ids: Set[str] = set()
        step_outputs: Dict[str, List[str]] = {}

        for step in steps:
            step_id = step.get("id")
            if not step_id:
                continue
            valid_step_ids.add(step_id)
            # Assume outputs are listed under 'outputs' key as a list of names
            outputs = step.get("outputs", [])
            if isinstance(outputs, list):
                step_outputs[step_id] = outputs
            else:
                step_outputs[step_id] = []

        # Fix references
        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> str | None:
        """
        Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        """
        if not candidates:
            return None
        # Use difflib to get close matches
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(
        workflow: dict[str, Any],
        valid_step_ids: Set[str],
        step_outputs: Dict[str, List[str]],
    ) -> None:
        """
        Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        steps = workflow.get("steps", [])
        for step in steps:
            params = step.get("parameters", {})
            if not isinstance(params, dict):
                continue
            for key, value in list(params.items()):
                if isinstance(value, str) and "." in value:
                    step_id, _, output_name = value.partition(".")
                    if step_id not in valid_step_ids:
                        # try to find best match for step id
                        best = ReferenceValidator._find_best_match(
                            step_id, list(valid_step_ids))
                        if best:
                            step_id = best
                        else:
                            # cannot resolve, skip
                            continue
                    # validate output name
                    outputs = step_outputs.get(step_id, [])
                    if output_name not in outputs:
                        # try to find best match for output name
                        best_out = ReferenceValidator._find_best_match(
                            output_name, outputs)
                        if best_out:
                            output_name = best_out
                        else:
                            # cannot resolve, skip
                            continue
                    # replace with resolved reference
                    params[key] = f"{step_id}.{output_name}"
            step["parameters"] = params

    @staticmethod
    def _fix_request_body_references(
        workflow: dict[str, Any],
        valid_step_ids: Set[str],
        step_outputs: Dict[str, List[str]],
    ) -> None:
        """
        Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        def _recurse(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: _recurse(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_recurse(v) for v in obj]
            if isinstance(obj, str) and "." in obj:
                step_id, _, output_name = obj.partition(".")
                if step_id not in valid_step_ids:
                    best = ReferenceValidator._find_best_match(
                        step_id, list(valid_step_ids))
                    if best:
                        step_id = best
                    else:
                        return obj
                outputs = step_outputs.get(step_id, [])
                if output_name not in outputs:
                    best_out = ReferenceValidator._find_best_match(
                        output_name, outputs)
                    if best_out:
                        output_name = best_out
                    else:
                        return obj
                return f"{step_id}.{output_name}"
            return obj

        steps = workflow.get("steps", [])
        for step in steps:
            body = step.get("request_body")
            if body is not None:
                step["request_body"] = _recurse(body)
