
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    result: Any

    def __str__(self) -> str:
        return f"MetricResult(name={self.metric_name}, params={self.metric_params}, result={self.result})"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        # Assume the main result is under the key 'result' in results_dict
        result = results_dict.get('result', results_dict)
        return cls(metric_name=metric_name, metric_params=metric_params, result=result)
