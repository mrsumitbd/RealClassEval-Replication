
from typing import Any
import difflib
import copy


class ReferenceValidator:

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
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
                step_outputs[step_id] = set(outputs)

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)
        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        steps = workflow.get("steps", [])
        for step in steps:
            parameters = step.get("parameters", {})
            for param_key, param_value in parameters.items():
                if isinstance(param_value, str) and param_value.startswith("{{") and param_value.endswith("}}"):
                    ref = param_value[2:-2].strip()
                    if "." in ref:
                        step_ref, output_ref = ref.split(".", 1)
                        if step_ref not in valid_step_ids:
                            best = ReferenceValidator._find_best_match(
                                step_ref, list(valid_step_ids))
                            if best:
                                # Try to fix the reference
                                if output_ref in step_outputs.get(best, set()):
                                    parameters[param_key] = f"{{{{{best}.{output_ref}}}}}"
                        else:
                            # Check if output_ref is valid
                            if output_ref not in step_outputs.get(step_ref, set()):
                                best_output = ReferenceValidator._find_best_match(
                                    output_ref, list(step_outputs.get(step_ref, set())))
                                if best_output:
                                    parameters[param_key] = f"{{{{{step_ref}.{best_output}}}}}"

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        steps = workflow.get("steps", [])
        for step in steps:
            request_body = step.get("request_body")
            if isinstance(request_body, dict):
                ReferenceValidator._fix_dict_references(
                    request_body, valid_step_ids, step_outputs)
            elif isinstance(request_body, str):
                # If the request_body is a string and contains a reference
                if request_body.startswith("{{") and request_body.endswith("}}"):
                    ref = request_body[2:-2].strip()
                    if "." in ref:
                        step_ref, output_ref = ref.split(".", 1)
                        if step_ref not in valid_step_ids:
                            best = ReferenceValidator._find_best_match(
                                step_ref, list(valid_step_ids))
                            if best:
                                if output_ref in step_outputs.get(best, set()):
                                    step["request_body"] = f"{{{{{best}.{output_ref}}}}}"
                        else:
                            if output_ref not in step_outputs.get(step_ref, set()):
                                best_output = ReferenceValidator._find_best_match(
                                    output_ref, list(step_outputs.get(step_ref, set())))
                                if best_output:
                                    step["request_body"] = f"{{{{{step_ref}.{best_output}}}}}"

    @staticmethod
    def _fix_dict_references(d: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        for k, v in d.items():
            if isinstance(v, dict):
                ReferenceValidator._fix_dict_references(
                    v, valid_step_ids, step_outputs)
            elif isinstance(v, str) and v.startswith("{{") and v.endswith("}}"):
                ref = v[2:-2].strip()
                if "." in ref:
                    step_ref, output_ref = ref.split(".", 1)
                    if step_ref not in valid_step_ids:
                        best = ReferenceValidator._find_best_match(
                            step_ref, list(valid_step_ids))
                        if best:
                            if output_ref in step_outputs.get(best, set()):
                                d[k] = f"{{{{{best}.{output_ref}}}}}"
                    else:
                        if output_ref not in step_outputs.get(step_ref, set()):
                            best_output = ReferenceValidator._find_best_match(
                                output_ref, list(step_outputs.get(step_ref, set())))
                            if best_output:
                                d[k] = f"{{{{{step_ref}.{best_output}}}}}"
