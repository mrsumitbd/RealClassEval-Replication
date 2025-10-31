
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    results_dict: Dict[str, Any]
    result_str: str = field(init=False)

    def __post_init__(self):
        self.result_str = f"Metric: {self.metric_name}, Params: {self.metric_params}, Results: {self.results_dict}"

    def __str__(self) -> str:
        return self.result_str

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        return cls(metric_name, metric_params, results_dict)
