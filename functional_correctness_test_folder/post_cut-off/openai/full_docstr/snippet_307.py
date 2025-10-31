
import re
import difflib
from typing import Any, Dict, List, Set, Union


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''

    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        '''Validate and fix step references in a workflow.
        This function checks all references to steps and their outputs in a workflow
        and fixes any inconsistencies.
        Args:
            workflow: The workflow to validate.
        Returns:
            The validated and fixed workflow.
        '''
        # Gather step ids and outputs
        steps = workflow.get('steps', {})
        valid_step_ids: Set[str] = set(steps.keys())
        step_outputs: Dict[str, List[str]] = {}
        for sid, step in steps.items():
            outputs = step.get('outputs', {})
            if isinstance(outputs, dict):
                step_outputs[sid] = list(outputs.keys())
            else:
                step_outputs[sid] = []

        # Fix references
        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Union[str, None]:
        '''Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        '''
        if not candidates:
            return None
        best = None
        best_ratio = 0.0
        for cand in candidates:
            ratio = difflib.SequenceMatcher(None, target, cand).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best = cand
        # Accept only if similarity is reasonable
        return best if best_ratio >= 0.6 else None

    @staticmethod
    def _replace_reference(match: re.Match, valid_step_ids: Set[str], step_outputs: Dict[str, List[str]]) -> str:
        ref = match.group(1).strip()
        # Split into step and optional output
        if '.' in ref:
            step_id, out_name = ref.split('.', 1)
        else:
            step_id, out_name = ref, None

        # Resolve step id
        if step_id not in valid_step_ids:
            step_id = ReferenceValidator._find_best_match(
                step_id, list(valid_step_ids))
            if step_id is None:
                return match.group(0)  # leave unchanged

        # Resolve output name
        if out_name:
            outputs = step_outputs.get(step_id, [])
            if out_name not in outputs:
                out_name = ReferenceValidator._find_best_match(
                    out_name, outputs)
                if out_name is None:
                    return match.group(0)  # leave unchanged
            return f"${{{step_id}.{out_name}}}"
        else:
            return f"${{{step_id}}}"

    @staticmethod
    def _fix_parameter_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, List[str]]) -> None:
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        param_pattern = re.compile(r'\${([^}]+)}')
        for step in workflow.get('steps', {}).values():
            params = step.get('parameters', {})
            if isinstance(params, dict):
                for key, value in params.items():
                    if isinstance(value, str):
                        new_val = param_pattern.sub(
                            lambda m: ReferenceValidator._replace_reference(
                                m, valid_step_ids, step_outputs),
                            value
                        )
                        step['parameters'][key] = new_val
            elif isinstance(params, list):
                for idx, item in enumerate(params):
                    if isinstance(item, str):
                        new_val = param_pattern.sub(
                            lambda m: ReferenceValidator._replace_reference(
                                m, valid_step_ids, step_outputs),
                            item
                        )
                        step['parameters'][idx] = new_val

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, List[str]]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        param_pattern = re.compile(r'\${([^}]+)}')

        def _process(value: Any) -> Any:
            if isinstance(value, str):
                return param_pattern.sub(
                    lambda m: ReferenceValidator._replace_reference(
                        m, valid_step_ids, step_outputs),
                    value
                )
            elif isinstance(value, dict):
                return {k: _process(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [_process(v) for v in value]
            return value

        for step in workflow.get('steps', {}).values():
            request = step.get('request')
            if not request:
                continue
            body = request.get('body')
            if body is not None:
                request['body'] = _process(body)
