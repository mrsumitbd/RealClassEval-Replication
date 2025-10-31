
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MetricResult:
    name: str
    params: Dict[str, Any]
    result: Any

    def __str__(self) -> str:
        return f"MetricResult(name={self.name}, params={self.params}, result={self.result})"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        result = results_dict.get(metric_name)
        return cls(metric_name, metric_params, result)
