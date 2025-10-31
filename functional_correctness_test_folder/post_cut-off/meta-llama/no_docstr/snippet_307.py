
from typing import Any, Dict, List, Set, Optional, Union


class ReferenceValidator:

    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        valid_step_ids = set(workflow['steps'].keys())
        step_outputs = {}

        for step_id, step in workflow['steps'].items():
            step_outputs[step_id] = step.get('out', [])

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        best_match = None
        max_ratio = 0

        for candidate in candidates:
            ratio = ReferenceValidator._levenshtein_ratio(target, candidate)
            if ratio > max_ratio:
                max_ratio = ratio
                best_match = candidate

        return best_match if max_ratio > 0.6 else None

    @staticmethod
    def _levenshtein_ratio(s1: str, s2: str) -> float:
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] +
                               1, dp[i - 1][j - 1] + cost)

        distance = dp[m][n]
        max_len = max(m, n)
        return 1 - distance / max_len

    @staticmethod
    def _fix_parameter_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        for step_id, step in workflow['steps'].items():
            if 'parameters' in step:
                for param, value in step['parameters'].items():
                    if isinstance(value, str) and value.startswith('$'):
                        ref = value[1:]
                        parts = ref.split('.')

                        if len(parts) == 2 and parts[0] in valid_step_ids:
                            step_id_ref = parts[0]
                            output_ref = parts[1]
                            if output_ref not in step_outputs[step_id_ref]:
                                best_match = ReferenceValidator._find_best_match(
                                    output_ref, step_outputs[step_id_ref])
                                if best_match:
                                    workflow['steps'][step_id]['parameters'][
                                        param] = f"${step_id_ref}.{best_match}"
                                else:
                                    workflow['steps'][step_id]['parameters'][param] = None

    @staticmethod
    def _fix_request_body_references(workflow: Dict[str, Any], valid_step_ids: Set[str], step_outputs: Dict[str, Any]) -> None:
        for step_id, step in workflow['steps'].items():
            if 'request_body' in step:
                request_body = step['request_body']
                if isinstance(request_body, dict):
                    for key, value in request_body.items():
                        if isinstance(value, str) and value.startswith('$'):
                            ref = value[1:]
                            parts = ref.split('.')

                            if len(parts) == 2 and parts[0] in valid_step_ids:
                                step_id_ref = parts[0]
                                output_ref = parts[1]
                                if output_ref not in step_outputs[step_id_ref]:
                                    best_match = ReferenceValidator._find_best_match(
                                        output_ref, step_outputs[step_id_ref])
                                    if best_match:
                                        workflow['steps'][step_id]['request_body'][
                                            key] = f"${step_id_ref}.{best_match}"
                                    else:
                                        workflow['steps'][step_id]['request_body'][key] = None
                elif isinstance(request_body, str) and request_body.startswith('$'):
                    ref = request_body[1:]
                    parts = ref.split('.')

                    if len(parts) == 2 and parts[0] in valid_step_ids:
                        step_id_ref = parts[0]
                        output_ref = parts[1]
                        if output_ref not in step_outputs[step_id_ref]:
                            best_match = ReferenceValidator._find_best_match(
                                output_ref, step_outputs[step_id_ref])
                            if best_match:
                                workflow['steps'][step_id]['request_body'] = f"${step_id_ref}.{best_match}"
                            else:
                                workflow['steps'][step_id]['request_body'] = None
