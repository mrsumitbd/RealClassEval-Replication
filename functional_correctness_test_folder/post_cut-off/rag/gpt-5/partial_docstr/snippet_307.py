from typing import Any, Dict, List, Set
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

        fixed_workflow = workflow  # modify in-place to preserve references

        steps = []
        if isinstance(fixed_workflow.get('workflow'), dict) and isinstance(fixed_workflow['workflow'].get('steps'), list):
            steps = fixed_workflow['workflow']['steps']
        elif isinstance(fixed_workflow.get('steps'), list):
            steps = fixed_workflow['steps']

        # Gather valid step IDs
        valid_step_ids: Set[str] = set()
        for step in steps:
            sid = step.get('id')
            if isinstance(sid, str) and sid:
                valid_step_ids.add(sid)

        # Gather outputs per step
        step_outputs: Dict[str, Set[str]] = {}
        for step in steps:
            sid = step.get('id')
            if not isinstance(sid, str) or not sid:
                continue
            outputs = step.get('outputs')
            output_names: Set[str] = set()
            if isinstance(outputs, dict):
                output_names.update(k for k in outputs.keys()
                                    if isinstance(k, str))
            elif isinstance(outputs, list):
                for item in outputs:
                    if isinstance(item, dict):
                        name = item.get('name')
                        if isinstance(name, str) and name:
                            output_names.add(name)
            step_outputs[sid] = output_names

        ReferenceValidator._fix_parameter_references(
            fixed_workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            fixed_workflow, valid_step_ids, step_outputs)

        return fixed_workflow

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
        steps = []
        if isinstance(workflow.get('workflow'), dict) and isinstance(workflow['workflow'].get('steps'), list):
            steps = workflow['workflow']['steps']
        elif isinstance(workflow.get('steps'), list):
            steps = workflow['steps']

        for step in steps:
            params = step.get('parameters')
            if params is not None:
                step['parameters'] = ReferenceValidator._fix_references_in_obj(
                    params, valid_step_ids, step_outputs
                )

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        steps = []
        if isinstance(workflow.get('workflow'), dict) and isinstance(workflow['workflow'].get('steps'), list):
            steps = workflow['workflow']['steps']
        elif isinstance(workflow.get('steps'), list):
            steps = workflow['steps']

        for step in steps:
            rb = step.get('requestBody')
            if rb is not None:
                step['requestBody'] = ReferenceValidator._fix_references_in_obj(
                    rb, valid_step_ids, step_outputs
                )

    # Regex patterns for references:
    # 1) JSON Pointer-like: "#/steps/<sid>/outputs/<out>"
    _PTR_RE = re.compile(r'(#/steps/)([^/]+)(/outputs/)([^/#\s]+)')
    # 2) Dot notation possibly with leading "$": "$?steps.<sid>.outputs.<out>"
    _DOT_RE = re.compile(
        r'(\$?steps\.)([A-Za-z0-9_\-]+)(\.outputs\.)([A-Za-z0-9_\-]+)')

    @staticmethod
    def _fix_references_in_obj(obj: Any, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> Any:
        if isinstance(obj, str):
            return ReferenceValidator._fix_references_in_string(obj, valid_step_ids, step_outputs)
        if isinstance(obj, list):
            for i, item in enumerate(obj):
                obj[i] = ReferenceValidator._fix_references_in_obj(
                    item, valid_step_ids, step_outputs)
            return obj
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                obj[k] = ReferenceValidator._fix_references_in_obj(
                    v, valid_step_ids, step_outputs)
            return obj
        return obj

    @staticmethod
    def _fix_references_in_string(s: str, valid_step_ids: set[str], step_outputs: dict[str, Any]) -> str:
        def fix_sid_out(sid: str, out: str) -> tuple[str, str]:
            new_sid = sid
            if sid not in valid_step_ids and valid_step_ids:
                best_sid = ReferenceValidator._find_best_match(
                    sid, list(valid_step_ids))
                if best_sid:
                    new_sid = best_sid
            new_out = out
            candidates = step_outputs.get(new_sid)
            if isinstance(candidates, set) and candidates:
                if out not in candidates:
                    best_out = ReferenceValidator._find_best_match(
                        out, list(candidates))
                    if best_out:
                        new_out = best_out
            return new_sid, new_out

        def repl_ptr(m: re.Match) -> str:
            pre, sid, mid, out = m.group(1), m.group(2), m.group(3), m.group(4)
            new_sid, new_out = fix_sid_out(sid, out)
            return f"{pre}{new_sid}{mid}{new_out}"

        def repl_dot(m: re.Match) -> str:
            pre, sid, mid, out = m.group(1), m.group(2), m.group(3), m.group(4)
            new_sid, new_out = fix_sid_out(sid, out)
            return f"{pre}{new_sid}{mid}{new_out}"

        s2 = ReferenceValidator._PTR_RE.sub(repl_ptr, s)
        s3 = ReferenceValidator._DOT_RE.sub(repl_dot, s2)
        return s3
