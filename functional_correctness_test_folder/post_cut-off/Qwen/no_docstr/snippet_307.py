
from typing import Any, Dict, List, Set, Optional


class ReferenceValidator:

    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        valid_step_ids = set(workflow.keys())
        step_outputs = {step_id: step.get('outputs', {})
                        for step_id, step in workflow.items()}

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        for candidate in candidates:
            if candidate.lower() == target.lower():
                return candidate
        return None

    @staticmethod
    def _fix_parameter_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        for step_id, step in workflow.items():
            parameters = step.get('parameters', {})
            for param_name, param_value in parameters.items():
                if isinstance(param_value, str) and param_value.startswith('${'):
                    target_step_id = param_value[2:-1]
                    best_match = ReferenceValidator._find_best_match(
                        target_step_id, list(valid_step_ids))
                    if best_match:
                        parameters[param_name] = f'${{{best_match}}}'
                    else:
                        raise ValueError(
                            f"Invalid reference {param_value} in step {step_id}")

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        for step_id, step in workflow.items():
            request_body = step.get('requestBody', {})
            if isinstance(request_body, dict):
                for key, value in request_body.items():
                    if isinstance(value, str) and value.startswith('${'):
                        target_step_id = value[2:-1]
                        best_match = ReferenceValidator._find_best_match(
                            target_step_id, list(valid_step_ids))
                        if best_match:
                            request_body[key] = f'${{{best_match}}}'
                        else:
                            raise ValueError(
                                f"Invalid reference {value} in step {step_id} request body")
