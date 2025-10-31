
import re
import difflib
from typing import Any, Dict, List, Set, Tuple, Union


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        """
        Validate and correct step references in the given workflow.
        Returns the workflow with references fixed.
        """
        steps = workflow.get("steps", [])
        valid_step_ids: Set[str] = {
            step.get("id") for step in steps if "id" in step}
        step_outputs: Dict[str, Any] = {
            step["id"]: step.get("outputs", {})
            for step in steps
            if "id" in step
        }

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
        best_candidate, best_ratio = None, 0.0
        for cand in candidates:
            ratio = difflib.SequenceMatcher(None, target, cand).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_candidate = cand
        # Threshold to avoid nonsense matches
        return best_candidate if best_ratio >= 0.6 else None

    @staticmethod
    def _fix_parameter_references(
        workflow: dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]
    ) -> None:
        """
        Fix parameter references in each step of the workflow.
        """
        for step in workflow.get("steps", []):
            if "parameters" in step:
                step["parameters"] = ReferenceValidator._replace_references_in_value(
                    step["parameters"], valid_step_ids, step_outputs
                )

    @staticmethod
    def _fix_request_body_references(
        workflow: dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]
    ) -> None:
        """
        Fix request body references in each step of the workflow.
        """
        for step in workflow.get("steps", []):
            request = step.get("request")
            if isinstance(request, dict) and "body" in request:
                request["body"] = ReferenceValidator._replace_references_in_value(
                    request["body"], valid_step_ids, step_outputs
                )

    @staticmethod
    def _replace_references_in_value(
        value: Any, valid_step_ids: Set[str], step_outputs: Dict[str, Any]
    ) -> Any:
        """
        Recursively replace references in a value (dict, list, or string).
        """
        if isinstance(value, dict):
            return {
                k: ReferenceValidator._replace_references_in_value(
                    v, valid_step_ids, step_outputs)
                for k, v in value.items()
            }
        if isinstance(value, list):
            return [
                ReferenceValidator._replace_references_in_value(
                    v, valid_step_ids, step_outputs)
                for v in value
            ]
        if isinstance(value, str):
            # Patterns: ${step_id.output_name} or {{step_id.output_name}}
            pattern = re.compile(r"(\${|{{)(\w+)\.(\w+)(}}|\})")

            def repl(match: re.Match) -> str:
                prefix, step_id, output_name, suffix = match.groups()
                # Validate step_id
                if step_id not in valid_step_ids:
                    best = ReferenceValidator._find_best_match(
                        step_id, list(valid_step_ids))
                    if best:
                        step_id = best
                # Validate output_name
                if step_id in step_outputs and output_name not in step_outputs[step_id]:
                    # If output missing, leave as is
                    return match.group(0)
                return f"{prefix}{step_id}.{output_name}{suffix}"
            return pattern.sub(repl, value)
        return value
