
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    results_dict: Dict[str, Any]

    def __str__(self) -> str:
        return f"MetricResult(metric_name={self.metric_name}, metric_params={self.metric_params}, results_dict={self.results_dict})"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        return cls(metric_name, metric_params, results_dict)
