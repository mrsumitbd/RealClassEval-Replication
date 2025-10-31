from typing import Any, Dict, List, Set
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
        steps = workflow.get("steps", [])
        valid_step_ids: Set[str] = set()
        step_outputs: Dict[str, Set[str]] = {}

        for step in steps:
            sid = step.get("id")
            if not isinstance(sid, str):
                continue
            valid_step_ids.add(sid)
            outputs = step.get("outputs")
            names: Set[str] = set()
            if isinstance(outputs, dict):
                names.update([k for k in outputs.keys() if isinstance(k, str)])
            elif isinstance(outputs, list):
                for item in outputs:
                    if isinstance(item, dict):
                        name = item.get("name")
                        if isinstance(name, str):
                            names.add(name)
                    elif isinstance(item, str):
                        names.add(item)
            step_outputs[sid] = names

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)  # type: ignore[arg-type]
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)  # type: ignore[arg-type]
        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> str | None:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates:
            return None
        if target in candidates:
            return target
        # Case-insensitive exact
        lower_map = {c.lower(): c for c in candidates}
        if target.lower() in lower_map:
            return lower_map[target.lower()]

        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        if matches:
            return matches[0]

        # Try case-insensitive fuzzy
        scores = []
        for c in candidates:
            ratio = difflib.SequenceMatcher(
                a=target.lower(), b=c.lower()).ratio()
            scores.append((ratio, c))
        scores.sort(reverse=True)
        return scores[0][1] if scores else None

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Set[str]]) -> None:
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        steps = workflow.get("steps", [])
        for step in steps:
            params = step.get("parameters")
            if params is not None:
                ReferenceValidator._traverse_and_fix(
                    params, valid_step_ids, step_outputs)

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Set[str]]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        steps = workflow.get("steps", [])
        for step in steps:
            rb = step.get("requestBody")
            if rb is not None:
                ReferenceValidator._traverse_and_fix(
                    rb, valid_step_ids, step_outputs)

    # ---------- Helpers (internal) ----------

    @staticmethod
    def _traverse_and_fix(node: Any, valid_step_ids: Set[str], step_outputs: Dict[str, Set[str]]) -> Any:
        # Recursively traverse dictionaries/lists and fix references in strings and $ref-like fields
        if isinstance(node, dict):
            # Handle $ref-like string values
            for k, v in list(node.items()):
                if isinstance(v, str):
                    # Fix mustache-like and ${{ }} refs within strings
                    node[k] = ReferenceValidator._fix_string_references(
                        v, valid_step_ids, step_outputs)
                    # Fix JSON pointer-like $ref paths
                    if k == "$ref" or "steps" in v:
                        node[k] = ReferenceValidator._fix_path_reference(
                            node[k], valid_step_ids, step_outputs)
                else:
                    node[k] = ReferenceValidator._traverse_and_fix(
                        v, valid_step_ids, step_outputs)
            return node
        elif isinstance(node, list):
            for i in range(len(node)):
                v = node[i]
                if isinstance(v, str):
                    fixed = ReferenceValidator._fix_string_references(
                        v, valid_step_ids, step_outputs)
                    fixed = ReferenceValidator._fix_path_reference(
                        fixed, valid_step_ids, step_outputs)
                    node[i] = fixed
                else:
                    node[i] = ReferenceValidator._traverse_and_fix(
                        v, valid_step_ids, step_outputs)
            return node
        elif isinstance(node, str):
            node = ReferenceValidator._fix_string_references(
                node, valid_step_ids, step_outputs)
            node = ReferenceValidator._fix_path_reference(
                node, valid_step_ids, step_outputs)
            return node
        else:
            return node

    @staticmethod
    def _fix_string_references(s: str, valid_step_ids: Set[str], step_outputs: Dict[str, Set[str]]) -> str:
        # Handle patterns like {{ steps.stepId.outputs.outputName }} and ${{ steps.stepId.outputs.outputName }}
        pattern = re.compile(
            r"(\$\s*)?\{\{\s*steps\.([A-Za-z0-9_\-]+)\.outputs\.([A-Za-z0-9_\-]+)\s*\}\}")

        def repl(m: re.Match) -> str:
            has_dollar = m.group(1) is not None
            step_id = m.group(2)
            out_name = m.group(3)
            fixed_step, fixed_out = ReferenceValidator._fix_pair(
                step_id, out_name, valid_step_ids, step_outputs)
            prefix = "${{ " if has_dollar else "{{ "
            return f"{prefix}steps.{fixed_step}.outputs.{fixed_out} }}"

        return pattern.sub(repl, s)

    @staticmethod
    def _fix_path_reference(s: str, valid_step_ids: Set[str], step_outputs: Dict[str, Set[str]]) -> str:
        # Fix JSON-pointer-like references containing /steps/<id>/outputs/<name>
        # Works for strings like "#/workflows/w/steps/stepA/outputs/result"
        if not isinstance(s, str) or "/steps/" not in s:
            return s
        try:
            parts = s.split("/")
            # find last occurrence of "steps" to be safe
            idxs = [i for i, p in enumerate(parts) if p == "steps"]
            if not idxs:
                return s
            idx = idxs[-1]
            step_id = parts[idx + 1] if idx + 1 < len(parts) else None
            outputs_literal = parts[idx + 2] if idx + 2 < len(parts) else None
            output_name = parts[idx + 3] if idx + 3 < len(parts) else None
            if step_id and outputs_literal == "outputs" and output_name:
                fixed_step, fixed_out = ReferenceValidator._fix_pair(
                    step_id, output_name, valid_step_ids, step_outputs)
                parts[idx + 1] = fixed_step
                parts[idx + 3] = fixed_out
                return "/".join(parts)
            return s
        except Exception:
            return s

    @staticmethod
    def _fix_pair(step_id: str, output_name: str, valid_step_ids: Set[str], step_outputs: Dict[str, Set[str]]) -> tuple[str, str]:
        # Fixes step_id and output_name to best matches, preserving originals when no match
        fixed_step = step_id
        if step_id not in valid_step_ids:
            best_step = ReferenceValidator._find_best_match(
                step_id, list(valid_step_ids))
            if best_step:
                fixed_step = best_step

        fixed_output = output_name
        outputs_for_step = step_outputs.get(fixed_step, set())
        if outputs_for_step:
            if output_name not in outputs_for_step:
                best_out = ReferenceValidator._find_best_match(
                    output_name, list(outputs_for_step))
                if best_out:
                    fixed_output = best_out
        return fixed_step, fixed_output
