
from typing import Any, Optional
import difflib


class ReferenceValidator:

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        valid_step_ids = {step["id"] for step in workflow["steps"]}
        step_outputs = {}
        for step in workflow["steps"]:
            if "outputs" in step:
                step_outputs[step["id"]] = step["outputs"]

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> Optional[str]:
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        for step in workflow["steps"]:
            if "parameters" in step:
                for param_name, param_value in step["parameters"].items():
                    if isinstance(param_value, str) and param_value.startswith("$."):
                        parts = param_value.split(".")
                        if len(parts) >= 3:
                            step_id = parts[1]
                            if step_id not in valid_step_ids:
                                best_match = ReferenceValidator._find_best_match(
                                    step_id, list(valid_step_ids))
                                if best_match:
                                    parts[1] = best_match
                                    step["parameters"][param_name] = ".".join(
                                        parts)

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        for step in workflow["steps"]:
            if "request" in step and "body" in step["request"]:
                body = step["request"]["body"]
                if isinstance(body, dict):
                    for key, value in body.items():
                        if isinstance(value, str) and value.startswith("$."):
                            parts = value.split(".")
                            if len(parts) >= 3:
                                step_id = parts[1]
                                if step_id not in valid_step_ids:
                                    best_match = ReferenceValidator._find_best_match(
                                        step_id, list(valid_step_ids))
                                    if best_match:
                                        parts[1] = best_match
                                        body[key] = ".".join(parts)
