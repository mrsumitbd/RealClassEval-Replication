
from typing import Any
import difflib
import copy
import re


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        workflow = copy.deepcopy(workflow)
        steps = workflow.get("steps", [])
        valid_step_ids = {step.get("id") for step in steps if "id" in step}
        step_outputs = {step.get("id"): step.get("outputs", {})
                        for step in steps if "id" in step}

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
        steps = workflow.get("steps", [])
        for step in steps:
            parameters = step.get("parameters", {})
            for param_key, param_value in parameters.items():
                if isinstance(param_value, str):
                    # Find all references in the form of {{steps.STEP_ID.outputs.OUTPUT}}
                    refs = re.findall(
                        r"\{\{steps\.([^.]+)\.outputs\.([^\}]+)\}\}", param_value)
                    for ref_step_id, ref_output in refs:
                        if ref_step_id not in valid_step_ids:
                            best_match = ReferenceValidator._find_best_match(
                                ref_step_id, list(valid_step_ids))
                            if best_match:
                                # Replace the wrong step id with the best match
                                old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                                new_ref = f"{{{{steps.{best_match}.outputs.{ref_output}}}}}"
                                parameters[param_key] = parameters[param_key].replace(
                                    old_ref, new_ref)
                        else:
                            # Check if output exists
                            outputs = step_outputs.get(ref_step_id, {})
                            if ref_output not in outputs:
                                best_output = ReferenceValidator._find_best_match(
                                    ref_output, list(outputs.keys()))
                                if best_output:
                                    old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                                    new_ref = f"{{{{steps.{ref_step_id}.outputs.{best_output}}}}}"
                                    parameters[param_key] = parameters[param_key].replace(
                                        old_ref, new_ref)
            step["parameters"] = parameters

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
            request_body = step.get("requestBody", None)
            if isinstance(request_body, str):
                refs = re.findall(
                    r"\{\{steps\.([^.]+)\.outputs\.([^\}]+)\}\}", request_body)
                for ref_step_id, ref_output in refs:
                    if ref_step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            ref_step_id, list(valid_step_ids))
                        if best_match:
                            old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                            new_ref = f"{{{{steps.{best_match}.outputs.{ref_output}}}}}"
                            request_body = request_body.replace(
                                old_ref, new_ref)
                    else:
                        outputs = step_outputs.get(ref_step_id, {})
                        if ref_output not in outputs:
                            best_output = ReferenceValidator._find_best_match(
                                ref_output, list(outputs.keys()))
                            if best_output:
                                old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                                new_ref = f"{{{{steps.{ref_step_id}.outputs.{best_output}}}}}"
                                request_body = request_body.replace(
                                    old_ref, new_ref)
                step["requestBody"] = request_body
            elif isinstance(request_body, dict):
                # Recursively fix references in dict
                ReferenceValidator._fix_dict_references(
                    request_body, valid_step_ids, step_outputs)

    @staticmethod
    def _fix_dict_references(d: dict, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        for k, v in d.items():
            if isinstance(v, str):
                refs = re.findall(
                    r"\{\{steps\.([^.]+)\.outputs\.([^\}]+)\}\}", v)
                for ref_step_id, ref_output in refs:
                    if ref_step_id not in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            ref_step_id, list(valid_step_ids))
                        if best_match:
                            old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                            new_ref = f"{{{{steps.{best_match}.outputs.{ref_output}}}}}"
                            d[k] = d[k].replace(old_ref, new_ref)
                    else:
                        outputs = step_outputs.get(ref_step_id, {})
                        if ref_output not in outputs:
                            best_output = ReferenceValidator._find_best_match(
                                ref_output, list(outputs.keys()))
                            if best_output:
                                old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                                new_ref = f"{{{{steps.{ref_step_id}.outputs.{best_output}}}}}"
                                d[k] = d[k].replace(old_ref, new_ref)
            elif isinstance(v, dict):
                ReferenceValidator._fix_dict_references(
                    v, valid_step_ids, step_outputs)
            elif isinstance(v, list):
                for idx, item in enumerate(v):
                    if isinstance(item, dict):
                        ReferenceValidator._fix_dict_references(
                            item, valid_step_ids, step_outputs)
                    elif isinstance(item, str):
                        refs = re.findall(
                            r"\{\{steps\.([^.]+)\.outputs\.([^\}]+)\}\}", item)
                        for ref_step_id, ref_output in refs:
                            if ref_step_id not in valid_step_ids:
                                best_match = ReferenceValidator._find_best_match(
                                    ref_step_id, list(valid_step_ids))
                                if best_match:
                                    old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                                    new_ref = f"{{{{steps.{best_match}.outputs.{ref_output}}}}}"
                                    v[idx] = v[idx].replace(old_ref, new_ref)
                            else:
                                outputs = step_outputs.get(ref_step_id, {})
                                if ref_output not in outputs:
                                    best_output = ReferenceValidator._find_best_match(
                                        ref_output, list(outputs.keys()))
                                    if best_output:
                                        old_ref = f"{{{{steps.{ref_step_id}.outputs.{ref_output}}}}}"
                                        new_ref = f"{{{{steps.{ref_step_id}.outputs.{best_output}}}}}"
                                        v[idx] = v[idx].replace(
                                            old_ref, new_ref)
