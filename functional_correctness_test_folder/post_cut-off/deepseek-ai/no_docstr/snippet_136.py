
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    results_dict: Dict[str, Any]

    def __str__(self) -> str:
        params_str = ", ".join(
            f"{k}={v}" for k, v in self.metric_params.items())
        results_str = ", ".join(
            f"{k}={v}" for k, v in self.results_dict.items())
        return f"{self.metric_name}({params_str}): {results_str}"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        return cls(metric_name, metric_params, results_dict)
