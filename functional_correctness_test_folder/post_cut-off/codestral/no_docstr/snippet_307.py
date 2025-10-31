
class ReferenceValidator:

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        valid_step_ids = set(workflow.keys())
        step_outputs = {step_id: set(
            output['name'] for output in step['outputs']) for step_id, step in workflow.items()}

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        for candidate in candidates:
            if candidate == target:
                return candidate
        for candidate in candidates:
            if candidate.lower() == target.lower():
                return candidate
        return None

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        for step_id, step in workflow.items():
            for parameter in step.get('parameters', []):
                if 'value' in parameter and isinstance(parameter['value'], str) and parameter['value'].startswith('{{'):
                    reference = parameter['value'][2:-2].strip()
                    if '.' in reference:
                        ref_step_id, ref_output = reference.split('.', 1)
                        if ref_step_id in valid_step_ids:
                            best_match = ReferenceValidator._find_best_match(
                                ref_output, step_outputs[ref_step_id])
                            if best_match:
                                parameter['value'] = f'{{{{{ref_step_id}.{best_match}}}}}'

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        for step_id, step in workflow.items():
            if 'request_body' in step and isinstance(step['request_body'], str) and step['request_body'].startswith('{{'):
                reference = step['request_body'][2:-2].strip()
                if '.' in reference:
                    ref_step_id, ref_output = reference.split('.', 1)
                    if ref_step_id in valid_step_ids:
                        best_match = ReferenceValidator._find_best_match(
                            ref_output, step_outputs[ref_step_id])
                        if best_match:
                            step['request_body'] = f'{{{{{ref_step_id}.{best_match}}}}}'
