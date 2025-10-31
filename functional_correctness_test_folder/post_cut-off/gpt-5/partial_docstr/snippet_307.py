from __future__ import annotations

import re
import difflib
from typing import Any, Iterable


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''
    _REF_PATTERN = re.compile(
        r"(steps\.)(?P<step>[A-Za-z0-9_\-]+)(\.outputs\.)(?P<out>[A-Za-z0-9_\-]+)")

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        report: dict[str, Any] = {
            "fixed": [],
            "warnings": [],
            "errors": [],
        }

        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            report["errors"].append("Workflow 'steps' should be a list.")
            return report

        # Build valid step ids and outputs mapping
        step_outputs: dict[str, set[str]] = {}
        valid_step_ids: set[str] = set()

        for step in steps:
            if not isinstance(step, dict):
                continue
            step_id = step.get("id")
            if isinstance(step_id, str) and step_id:
                valid_step_ids.add(step_id)
                outputs = step.get("outputs", {})
                output_keys: set[str] = set()
                if isinstance(outputs, dict):
                    output_keys = set(map(str, outputs.keys()))
                elif isinstance(outputs, list):
                    for item in outputs:
                        if isinstance(item, dict):
                            if "name" in item and isinstance(item["name"], str):
                                output_keys.add(item["name"])
                            elif "id" in item and isinstance(item["id"], str):
                                output_keys.add(item["id"])
                step_outputs[step_id] = output_keys

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs, report)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs, report)
        return report

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
        # Try a direct match first
        if target in candidates:
            return target
        # Use difflib to find the closest match
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(
        workflow: dict[str, Any],
        valid_step_ids: set[str],
        step_outputs: dict[str, Any],
        report: dict[str, Any] | None = None,
    ) -> None:
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return

        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            params = step.get("parameters")
            if params is not None:
                ReferenceValidator._walk_and_fix_container(
                    params,
                    path_prefix=f"steps[{idx}].parameters",
                    valid_step_ids=valid_step_ids,
                    step_outputs=step_outputs,
                    report=report,
                )

    @staticmethod
    def _fix_request_body_references(
        workflow: dict[str, Any],
        valid_step_ids: set[str],
        step_outputs: dict[str, Any],
        report: dict[str, Any] | None = None,
    ) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return

        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue

            # Common places for body-like content
            # 1) requestBody (OpenAPI-like)
            if "requestBody" in step:
                ReferenceValidator._walk_and_fix_container(
                    step["requestBody"],
                    path_prefix=f"steps[{idx}].requestBody",
                    valid_step_ids=valid_step_ids,
                    step_outputs=step_outputs,
                    report=report,
                )

            # 2) request -> body (generic)
            req = step.get("request")
            if isinstance(req, dict) and "body" in req:
                ReferenceValidator._walk_and_fix_container(
                    req["body"],
                    path_prefix=f"steps[{idx}].request.body",
                    valid_step_ids=valid_step_ids,
                    step_outputs=step_outputs,
                    report=report,
                )

    # Internal helpers

    @staticmethod
    def _walk_and_fix_container(
        container: Any,
        path_prefix: str,
        valid_step_ids: set[str],
        step_outputs: dict[str, set[str]],
        report: dict[str, Any] | None,
    ) -> None:
        # Traverse dict/list structures and fix any string values found
        if isinstance(container, dict):
            for k, v in list(container.items()):
                sub_path = f"{path_prefix}.{k}"
                if isinstance(v, (dict, list)):
                    ReferenceValidator._walk_and_fix_container(
                        v, sub_path, valid_step_ids, step_outputs, report
                    )
                elif isinstance(v, str):
                    new_v, changes = ReferenceValidator._fix_references_in_string(
                        v, valid_step_ids, step_outputs
                    )
                    if new_v != v:
                        container[k] = new_v
                        if report is not None:
                            for change in changes:
                                change_record = {
                                    "path": sub_path,
                                    "original": v,
                                    "updated": new_v,
                                    "detail": change,
                                }
                                report["fixed"].append(change_record)
        elif isinstance(container, list):
            for i, item in enumerate(list(container)):
                sub_path = f"{path_prefix}[{i}]"
                if isinstance(item, (dict, list)):
                    ReferenceValidator._walk_and_fix_container(
                        item, sub_path, valid_step_ids, step_outputs, report
                    )
                elif isinstance(item, str):
                    new_item, changes = ReferenceValidator._fix_references_in_string(
                        item, valid_step_ids, step_outputs
                    )
                    if new_item != item:
                        container[i] = new_item
                        if report is not None:
                            for change in changes:
                                change_record = {
                                    "path": sub_path,
                                    "original": item,
                                    "updated": new_item,
                                    "detail": change,
                                }
                                report["fixed"].append(change_record)

    @staticmethod
    def _fix_references_in_string(
        value: str,
        valid_step_ids: set[str],
        step_outputs: dict[str, set[str]],
    ) -> tuple[str, list[str]]:
        # Looks for occurrences of steps.<stepId>.outputs.<outputKey> anywhere inside the string
        # and attempts to fix stepId and outputKey to known values.
        changes: list[str] = []
        new_value = value
        offset = 0  # account for length differences as we replace

        for match in list(ReferenceValidator._REF_PATTERN.finditer(value)):
            start, end = match.span()
            start += offset
            end += offset

            current_segment = new_value[start:end]
            seg_match = ReferenceValidator._REF_PATTERN.match(current_segment)
            if not seg_match:
                continue

            step_id = seg_match.group("step")
            output_key = seg_match.group("out")

            new_step_id = step_id
            if step_id not in valid_step_ids:
                best_step = ReferenceValidator._find_best_match(
                    step_id, sorted(valid_step_ids))
                if best_step is not None and best_step != step_id:
                    new_step_id = best_step
                    changes.append(
                        f"Rewrote step id '{step_id}' -> '{new_step_id}'.")

            available_outputs: set[str] = step_outputs.get(new_step_id, set())
            new_output_key = output_key
            if available_outputs and output_key not in available_outputs:
                best_out = ReferenceValidator._find_best_match(
                    output_key, sorted(available_outputs))
                if best_out is not None and best_out != output_key:
                    new_output_key = best_out
                    changes.append(
                        f"Rewrote output key '{output_key}' -> '{new_output_key}' for step '{new_step_id}'.")

            if new_step_id != step_id or new_output_key != output_key:
                replaced_segment = f"steps.{new_step_id}.outputs.{new_output_key}"
                new_value = new_value[:start] + \
                    replaced_segment + new_value[end:]
                # Update offset for subsequent matches (original match length may differ)
                offset += len(replaced_segment) - (end - start)

        return new_value, changes

    @staticmethod
    def _flatten(iterable: Iterable[Iterable[Any]]) -> list[Any]:
        return [x for sub in iterable for x in sub]
