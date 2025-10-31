import difflib
from typing import Any

class ReferenceValidator:
    """Validates and fixes step references in Arazzo workflows."""

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        """Validate and fix step references in a workflow.

        This function checks all references to steps and their outputs in a workflow
        and fixes any inconsistencies.

        Args:
            workflow: The workflow to validate.

        Returns:
            The validated and fixed workflow.
        """
        if not workflow or 'steps' not in workflow:
            return workflow
        valid_step_ids = {step['stepId'] for step in workflow['steps'] if 'stepId' in step}
        step_outputs = {}
        for step in workflow['steps']:
            if 'stepId' in step:
                step_id = step['stepId']
                outputs = step.get('outputs', {})
                output_names = []
                for output_name in outputs.keys():
                    output_names.append(output_name)
                step_outputs[step_id] = output_names
        ReferenceValidator._fix_parameter_references(workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(workflow, valid_step_ids, step_outputs)
        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        """Find the best matching string from a list of candidates using sequence matching.

        Args:
            target: The target string to match.
            candidates: List of candidate strings.

        Returns:
            The best matching string or None if candidates is empty.
        """
        if not candidates:
            return None
        similarities = [(candidate, difflib.SequenceMatcher(None, target, candidate).ratio()) for candidate in candidates]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[0][0]

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        """Fix parameter references in a workflow.

        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        for step in workflow['steps']:
            for param in step.get('parameters', []):
                value = param.get('value', '')
                if isinstance(value, str) and value.startswith('$steps.'):
                    try:
                        parts = value.split('.')
                        if len(parts) >= 4:
                            ref_step_id = parts[1]
                            output_name = parts[3]
                            base_output_name = output_name
                            if '.' in output_name:
                                base_output_name = output_name.split('.', 1)[0]
                            if ref_step_id not in valid_step_ids:
                                for valid_id in valid_step_ids:
                                    if ref_step_id in valid_id or valid_id in ref_step_id:
                                        logger.warning(f"Fixing invalid step reference: '{ref_step_id}' -> '{valid_id}'")
                                        parts[1] = valid_id
                                        ref_step_id = valid_id
                                        param['value'] = '.'.join(parts)
                                        break
                            if ref_step_id in step_outputs and base_output_name not in step_outputs[ref_step_id]:
                                valid_outputs = list(step_outputs[ref_step_id])
                                best_match = ReferenceValidator._find_best_match(base_output_name, valid_outputs)
                                if best_match:
                                    logger.warning(f"Fixing invalid output reference: '{output_name}' -> '{best_match}'")
                                    if '.' in output_name:
                                        suffix = output_name.split('.', 1)[1]
                                        new_output = f'{best_match}.{suffix}'
                                    else:
                                        new_output = best_match
                                    parts[3] = new_output
                                    param['value'] = '.'.join(parts)
                    except Exception as e:
                        logger.warning(f"Error validating step reference '{value}': {e}")

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        """Fix request body references in a workflow.

        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        for step in workflow['steps']:
            if 'requestBody' in step and 'payload' in step['requestBody']:
                value = step['requestBody']['payload']
                if isinstance(value, str) and value.startswith('$steps.'):
                    try:
                        parts = value.split('.')
                        if len(parts) >= 4:
                            ref_step_id = parts[1]
                            output_name = parts[3]
                            base_output_name = output_name
                            if '.' in output_name:
                                base_output_name = output_name.split('.', 1)[0]
                            if ref_step_id not in valid_step_ids:
                                for valid_id in valid_step_ids:
                                    if ref_step_id in valid_id or valid_id in ref_step_id:
                                        logger.warning(f"Fixing invalid step reference in requestBody: '{ref_step_id}' -> '{valid_id}'")
                                        parts[1] = valid_id
                                        ref_step_id = valid_id
                                        step['requestBody']['payload'] = '.'.join(parts)
                                        break
                            if ref_step_id in step_outputs and base_output_name not in step_outputs[ref_step_id]:
                                valid_outputs = list(step_outputs[ref_step_id])
                                best_match = ReferenceValidator._find_best_match(base_output_name, valid_outputs)
                                if best_match:
                                    logger.warning(f"Fixing invalid output reference in requestBody: '{output_name}' -> '{best_match}'")
                                    if '.' in output_name:
                                        suffix = output_name.split('.', 1)[1]
                                        new_output = f'{best_match}.{suffix}'
                                    else:
                                        new_output = best_match
                                    parts[3] = new_output
                                    step['requestBody']['payload'] = '.'.join(parts)
                    except Exception as e:
                        logger.warning(f"Error validating step reference in requestBody '{value}': {e}")