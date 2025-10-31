
import re
import difflib
from typing import Any, Dict, List, Set, Union


class ReferenceValidator:
    '''Validates and fixes step references in Arazzo workflows.'''

    _REFERENCE_RE = re.compile(r'\${?([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)}?')

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
        # Collect step ids and outputs
        steps = workflow.get('steps', {})
        valid_step_ids: Set[str] = set()
        step_outputs: Dict[str, List[str]] = {}

        for step_id, step in steps.items():
            valid_step_ids.add(step_id)
            # Assume outputs are listed under 'outputs' key as a list of names
            outputs = step.get('outputs', [])
            if isinstance(outputs, list):
                step_outputs[step_id] = outputs
            else:
                step_outputs[step_id] = []

        # Fix references
        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

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
        best = None
        best_ratio = 0.0
        for cand in candidates:
            ratio = difflib.SequenceMatcher(None, target, cand).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best = cand
        # Accept only if ratio is reasonably high
        return best if best_ratio >= 0.6 else None

    @staticmethod
    def _replace_reference(match: re.Match, valid_step_ids: Set[str], step_outputs: Dict[str, List[str]]) -> str:
        step_id, output_name = match.group(1), match.group(2)
        # Validate step id
        if step_id not in valid_step_ids:
            # Try to find best match
            new_step_id = ReferenceValidator._find_best_match(
                step_id, list(valid_step_ids))
            if new_step_id:
                step_id = new_step_id
            else:
                # Cannot resolve, leave as is
                return match.group(0)
        # Validate output name
        outputs = step_outputs.get(step_id, [])
        if output_name not in outputs:
            # Try to find best match
            new_output = ReferenceValidator._find_best_match(
                output_name, outputs)
            if new_output:
                output_name = new_output
            else:
                # Cannot resolve, leave as is
                return match.group(0)
        return f'{step_id}.{output_name}'

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        steps = workflow.get('steps', {})
        for step in steps.values():
            params = step.get('parameters', {})
            if not isinstance(params, dict):
                continue
            for key, value in params.items():
                if isinstance(value, str):
                    new_value = ReferenceValidator._REFERENCE_RE.sub(
                        lambda m: ReferenceValidator._replace_reference(
                            m, valid_step_ids, step_outputs),
                        value
                    )
                    params[key] = new_value
                elif isinstance(value, list):
                    # Handle list of strings
                    new_list = []
                    for item in value:
                        if isinstance(item, str):
                            new_item = ReferenceValidator._REFERENCE_RE.sub(
                                lambda m: ReferenceValidator._replace_reference(
                                    m, valid_step_ids, step_outputs),
                                item
                            )
                            new_list.append(new_item)
                        else:
                            new_list.append(item)
                    params[key] = new_list
                elif isinstance(value, dict):
                    # Nested dict: apply recursively
                    ReferenceValidator._fix_parameter_references(
                        {'parameters': value}, valid_step_ids, step_outputs
                    )
                    params[key] = value

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        '''Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        '''
        def _recursive_fix(obj: Any) -> Any:
            if isinstance(obj, str):
                return ReferenceValidator._REFERENCE_RE.sub(
                    lambda m: ReferenceValidator._replace_reference(
                        m, valid_step_ids, step_outputs),
                    obj
                )
            if isinstance(obj, list):
                return [_recursive_fix(item) for item in obj]
            if isinstance(obj, dict):
                return {k: _recursive_fix(v) for k, v in obj.items()}
            return obj

        steps = workflow.get('steps', {})
        for step in steps.values():
            body = step.get('request_body')
            if body is not None:
                step['request_body'] = _recursive_fix(body)
