from typing import Any
import copy
import difflib
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
        if not isinstance(workflow, dict):
            return workflow

        wf = workflow  # modify in place per common expectations

        # Resolve steps container
        steps = wf.get("steps")
        if steps is None and isinstance(wf.get("workflow"), dict):
            steps = wf["workflow"].get("steps")

        if not isinstance(steps, list):
            return wf

        # Build valid step IDs
        valid_step_ids: set[str] = set()
        for step in steps:
            sid = step.get("id") if isinstance(step, dict) else None
            if isinstance(sid, str) and sid:
                valid_step_ids.add(sid)

        # Build a map of step_id -> output names (best-effort)
        step_outputs: dict[str, set[str]] = {}
        for step in steps:
            if not isinstance(step, dict):
                continue
            sid = step.get("id")
            if not isinstance(sid, str):
                continue
            outputs: set[str] = set()

            # Common patterns
            outs = step.get("outputs")
            if isinstance(outs, dict):
                outputs.update(str(k) for k in outs.keys())
            elif isinstance(outs, list):
                for item in outs:
                    if isinstance(item, dict):
                        name = item.get("name")
                        if isinstance(name, str):
                            outputs.add(name)

            # Heuristic: some workflows may define output schemas
            out_obj = step.get("output")
            if isinstance(out_obj, dict):
                props = out_obj.get("properties")
                if isinstance(props, dict):
                    outputs.update(str(k) for k in props.keys())

            # Another heuristic: responseMappings/outputMappings as dict of names
            for key in ("responseMappings", "outputMappings", "mappings"):
                maps = step.get(key)
                if isinstance(maps, dict):
                    outputs.update(str(k) for k in maps.keys())

            step_outputs[sid] = outputs

        # Fix dependencies between steps: dependsOn as str or list
        for step in steps:
            if not isinstance(step, dict):
                continue
            depends = step.get("dependsOn")
            if isinstance(depends, str):
                if depends not in valid_step_ids:
                    match = ReferenceValidator._find_best_match(
                        depends, list(valid_step_ids))
                    if match:
                        step["dependsOn"] = match
            elif isinstance(depends, list):
                new_depends = []
                changed = False
                for d in depends:
                    if isinstance(d, str):
                        if d in valid_step_ids:
                            new_depends.append(d)
                        else:
                            match = ReferenceValidator._find_best_match(
                                d, list(valid_step_ids))
                            new_depends.append(match if match else d)
                            changed = changed or (match is not None)
                    else:
                        new_depends.append(d)
                if changed:
                    step["dependsOn"] = new_depends

        # Fix parameters and request bodies
        ReferenceValidator._fix_parameter_references(
            wf, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            wf, valid_step_ids, step_outputs)

        return wf

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates or not isinstance(target, str) or not target:
            return None

        # Lowercase map for case-insensitive matching, but return original casing
        lower_map = {c.lower(): c for c in candidates}
        target_l = target.lower()
        close = difflib.get_close_matches(
            target_l, list(lower_map.keys()), n=1, cutoff=0.6)
        if close:
            return lower_map[close[0]]

        # Fall back to highest ratio manually if cutoff too strict
        best_candidate = None
        best_ratio = 0.0
        for c in candidates:
            ratio = difflib.SequenceMatcher(a=target_l, b=c.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_candidate = c
        return best_candidate

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        if not isinstance(workflow, dict):
            return

        steps = workflow.get("steps")
        if steps is None and isinstance(workflow.get("workflow"), dict):
            steps = workflow["workflow"].get("steps")

        if not isinstance(steps, list):
            return

        def outputs_for(step_id: str) -> set[str]:
            outs = step_outputs.get(step_id)
            if isinstance(outs, (set, list, tuple)):
                return set(outs)
            if isinstance(outs, dict):
                return set(outs.keys())
            return set()

        # Pattern to find step output references, optionally wrapped in {{ }} or ${{ }}
        # We will replace only the "steps.<step>.outputs.<out>" segment inside the match.
        ref_pattern = re.compile(
            r'(?P<full>(?P<prefix>\{\{\s*|\$\{\{\s*)?'
            r'(?P<core>steps\.(?P<step>[A-Za-z0-9_\-\.]+)\.outputs\.(?P<out>[A-Za-z0-9_\-\.]+))'
            r'\s*(?P<suffix>\}\})?)'
        )

        step_ref_keys = {"fromStep", "step", "from", "sourceStep", "refStep"}
        output_ref_keys = {"select", "output",
                           "path", "key", "property", "attribute"}

        def fix_string_refs(s: str) -> str:
            def _repl(m: re.Match) -> str:
                full = m.group("full")
                core = m.group("core")
                step_id = m.group("step")
                out_name = m.group("out")

                new_step = step_id
                if step_id not in valid_step_ids:
                    match = ReferenceValidator._find_best_match(
                        step_id, list(valid_step_ids))
                    if match:
                        new_step = match

                candidates = outputs_for(new_step)
                new_out = out_name
                if candidates and out_name not in candidates:
                    match_out = ReferenceValidator._find_best_match(
                        out_name, list(candidates))
                    if match_out:
                        new_out = match_out

                new_core = f"steps.{new_step}.outputs.{new_out}"
                return full.replace(core, new_core)

            if not isinstance(s, str) or "steps." not in s or ".outputs." not in s:
                return s
            try:
                return ref_pattern.sub(_repl, s)
            except Exception:
                return s

        def traverse_and_fix(obj: Any) -> Any:
            if isinstance(obj, str):
                return fix_string_refs(obj)
            if isinstance(obj, list):
                return [traverse_and_fix(x) for x in obj]
            if isinstance(obj, dict):
                # If this dict directly denotes a "valueFrom" like structure, fix targeted keys first.
                # Then recurse for all other values.
                # Fix step reference keys
                local_step_value = None
                for k in list(obj.keys()):
                    v = obj[k]
                    if k in step_ref_keys and isinstance(v, str):
                        if v not in valid_step_ids:
                            match = ReferenceValidator._find_best_match(
                                v, list(valid_step_ids))
                            if match:
                                obj[k] = match
                                local_step_value = match
                            else:
                                local_step_value = v
                        else:
                            local_step_value = v

                # Fix output reference keys based on associated step if available
                if local_step_value:
                    outs = outputs_for(local_step_value)
                    if outs:
                        for k in list(obj.keys()):
                            if k in output_ref_keys and isinstance(obj[k], str):
                                out_v = obj[k]
                                if out_v not in outs:
                                    match_out = ReferenceValidator._find_best_match(
                                        out_v, list(outs))
                                    if match_out:
                                        obj[k] = match_out

                # Recurse for all values
                for k, v in list(obj.items()):
                    obj[k] = traverse_and_fix(v)
                return obj
            return obj

            # End traverse_and_fix

        # Walk over likely parameter containers per step
        for step in steps:
            if not isinstance(step, dict):
                continue

            for key in ("parameters", "params", "inputs"):
                if key in step:
                    step[key] = traverse_and_fix(step[key])

            # Sometimes parameters are nested in "request" object as query/path/header params
            req = step.get("request")
            if isinstance(req, dict):
                for key in ("parameters", "params", "query", "headers", "path"):
                    if key in req:
                        req[key] = traverse_and_fix(req[key])

            # Also fix any generic "valueFrom"-like structures directly on the step
            for k in list(step.keys()):
                if k.lower() in ("valuefrom", "value_from", "source", "from"):
                    step[k] = traverse_and_fix(step[k])

            # As a safe catch-all, fix any string in step which contains step output refs
            for k, v in list(step.items()):
                if isinstance(v, str):
                    step[k] = traverse_and_fix(v)

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        if not isinstance(workflow, dict):
            return

        steps = workflow.get("steps")
        if steps is None and isinstance(workflow.get("workflow"), dict):
            steps = workflow["workflow"].get("steps")

        if not isinstance(steps, list):
            return

        def outputs_for(step_id: str) -> set[str]:
            outs = step_outputs.get(step_id)
            if isinstance(outs, (set, list, tuple)):
                return set(outs)
            if isinstance(outs, dict):
                return set(outs.keys())
            return set()

        ref_pattern = re.compile(
            r'(?P<full>(?P<prefix>\{\{\s*|\$\{\{\s*)?'
            r'(?P<core>steps\.(?P<step>[A-Za-z0-9_\-\.]+)\.outputs\.(?P<out>[A-Za-z0-9_\-\.]+))'
            r'\s*(?P<suffix>\}\})?)'
        )

        step_ref_keys = {"fromStep", "step", "from", "sourceStep", "refStep"}
        output_ref_keys = {"select", "output",
                           "path", "key", "property", "attribute"}

        def fix_string_refs(s: str) -> str:
            def _repl(m: re.Match) -> str:
                full = m.group("full")
                core = m.group("core")
                step_id = m.group("step")
                out_name = m.group("out")

                new_step = step_id
                if step_id not in valid_step_ids:
                    match = ReferenceValidator._find_best_match(
                        step_id, list(valid_step_ids))
                    if match:
                        new_step = match

                candidates = outputs_for(new_step)
                new_out = out_name
                if candidates and out_name not in candidates:
                    match_out = ReferenceValidator._find_best_match(
                        out_name, list(candidates))
                    if match_out:
                        new_out = match_out

                new_core = f"steps.{new_step}.outputs.{new_out}"
                return full.replace(core, new_core)

            if not isinstance(s, str) or "steps." not in s or ".outputs." not in s:
                return s
            try:
                return ref_pattern.sub(_repl, s)
            except Exception:
                return s

        def traverse_and_fix(obj: Any) -> Any:
            if isinstance(obj, str):
                return fix_string_refs(obj)
            if isinstance(obj, list):
                return [traverse_and_fix(x) for x in obj]
            if isinstance(obj, dict):
                # Handle dictionaries that encode "valueFrom"-like structures
                local_step_value = None
                for k in list(obj.keys()):
                    v = obj[k]
                    if k in step_ref_keys and isinstance(v, str):
                        if v not in valid_step_ids:
                            match = ReferenceValidator._find_best_match(
                                v, list(valid_step_ids))
                            if match:
                                obj[k] = match
                                local_step_value = match
                            else:
                                local_step_value = v
                        else:
                            local_step_value = v

                if local_step_value:
                    outs = outputs_for(local_step_value)
                    if outs:
                        for k in list(obj.keys()):
                            if k in output_ref_keys and isinstance(obj[k], str):
                                out_v = obj[k]
                                if out_v not in outs:
                                    match_out = ReferenceValidator._find_best_match(
                                        out_v, list(outs))
                                    if match_out:
                                        obj[k] = match_out

                for k, v in list(obj.items()):
                    obj[k] = traverse_and_fix(v)
                return obj
            return obj

        for step in steps:
            if not isinstance(step, dict):
                continue

            # Direct requestBody
            if "requestBody" in step:
                step["requestBody"] = traverse_and_fix(step["requestBody"])

            # Some structures may place body inside "request" object
            req = step.get("request")
            if isinstance(req, dict):
                if "body" in req:
                    req["body"] = traverse_and_fix(req["body"])
                if "requestBody" in req:
                    req["requestBody"] = traverse_and_fix(req["requestBody"])

            # Also check "payload" or "data" fields commonly used
            for key in ("payload", "data", "json", "form", "formData"):
                if key in step:
                    step[key] = traverse_and_fix(step[key])
