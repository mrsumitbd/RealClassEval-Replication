from __future__ import annotations

import re
from difflib import get_close_matches
from typing import Any


class ReferenceValidator:
    _REF_PATTERNS = [
        re.compile(r"\{\{\s*steps\.([^.}\s]+)\.([^\s}]+)\s*\}\}"),
        re.compile(r"\$\{\{\s*steps\.([^.}\s]+)\.([^\s}]+)\s*\}\}"),
    ]

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return workflow

        valid_step_ids: set[str] = set()
        for s in steps:
            sid = s.get("id")
            if isinstance(sid, str) and sid:
                valid_step_ids.add(sid)

        step_outputs: dict[str, set[str]] = {}
        for s in steps:
            sid = s.get("id")
            if not isinstance(sid, str) or not sid:
                continue
            outputs: set[str] = set()
            # Collect outputs from various commonly used keys
            # 1) explicit list under "outputs"
            outs = s.get("outputs")
            if isinstance(outs, list):
                for o in outs:
                    if isinstance(o, str) and o:
                        outputs.add(o)
            # 2) mapping/dict under "outputs"
            elif isinstance(outs, dict):
                for k in outs.keys():
                    if isinstance(k, str) and k:
                        outputs.add(k)
            # 3) response mapping
            resp = s.get("response")
            if isinstance(resp, dict):
                for k in resp.keys():
                    if isinstance(k, str) and k:
                        outputs.add(k)
            # 4) generic "result" fields hinted
            for k in ("output", "result", "body", "data", "response"):
                if k in s:
                    outputs.add(k)
            if not outputs:
                outputs = {"output", "result"}
            step_outputs[sid] = outputs

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)
        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        if not target or not candidates:
            return None
        if target in candidates:
            return target
        matches = get_close_matches(target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return

        for step in steps:
            for key in ("parameters", "params", "args"):
                if key in step:
                    step[key] = ReferenceValidator._fix_in_obj(
                        step[key], valid_step_ids, step_outputs
                    )

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return

        for step in steps:
            # Common places where request body might be stored
            candidates = [
                "requestBody",
                "request_body",
                "body",
                ("request", "body"),
                ("http", "body"),
            ]
            for key in candidates:
                if isinstance(key, tuple):
                    obj = step
                    exists = True
                    for k in key:
                        if isinstance(obj, dict) and k in obj:
                            obj = obj[k]
                        else:
                            exists = False
                            break
                    if exists:
                        # Replace nested body with fixed version
                        fixed = ReferenceValidator._fix_in_obj(
                            obj, valid_step_ids, step_outputs)
                        # Reassign into nested structure
                        tgt = step
                        for k in key[:-1]:
                            tgt = tgt[k]
                        tgt[key[-1]] = fixed
                else:
                    if key in step:
                        step[key] = ReferenceValidator._fix_in_obj(
                            step[key], valid_step_ids, step_outputs)

    @staticmethod
    def _fix_in_obj(obj: Any, valid_step_ids: set[str], step_outputs: dict[str, set[str]]) -> Any:
        if isinstance(obj, str):
            return ReferenceValidator._fix_in_string(obj, valid_step_ids, step_outputs)
        if isinstance(obj, list):
            return [ReferenceValidator._fix_in_obj(v, valid_step_ids, step_outputs) for v in obj]
        if isinstance(obj, dict):
            return {k: ReferenceValidator._fix_in_obj(v, valid_step_ids, step_outputs) for k, v in obj.items()}
        return obj

    @staticmethod
    def _fix_in_string(s: str, valid_step_ids: set[str], step_outputs: dict[str, set[str]]) -> str:
        def replace(match: re.Match) -> str:
            original = match.group(0)
            sid = match.group(1)
            out = match.group(2)

            matched_id = sid if sid in valid_step_ids else ReferenceValidator._find_best_match(
                sid, list(valid_step_ids))
            if not matched_id:
                return original  # cannot fix step id, leave as is

            outputs = list(step_outputs.get(matched_id, {"output", "result"}))
            matched_out = out if out in outputs else ReferenceValidator._find_best_match(
                out, outputs)
            if not matched_out:
                return original  # cannot fix output, leave as is

            # Preserve the wrapper style based on the matched pattern
            text = match.group(0)
            if text.startswith("${{"):
                return f"${{{{ steps.{matched_id}.{matched_out} }}}}"
            return f"{{{{ steps.{matched_id}.{matched_out} }}}}"

        new_s = s
        for pat in ReferenceValidator._REF_PATTERNS:
            new_s = pat.sub(replace, new_s)
        return new_s
