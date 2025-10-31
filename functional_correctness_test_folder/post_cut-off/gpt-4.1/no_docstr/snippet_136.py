
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    results_dict: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        params_str = ', '.join(
            f"{k}={v}" for k, v in self.metric_params.items())
        results_str = ', '.join(
            f"{k}={v}" for k, v in self.results_dict.items())
        return f"MetricResult(metric_name='{self.metric_name}', params={{ {params_str} }}, results={{ {results_str} }})"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        return cls(metric_name=metric_name, metric_params=metric_params, results_dict=results_dict)
