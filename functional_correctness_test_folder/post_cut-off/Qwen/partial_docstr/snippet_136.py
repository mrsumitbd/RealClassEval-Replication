
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    results_dict: Dict[str, Any]
    result: Any = field(init=False)

    def __post_init__(self):
        self.result = self._compute_result()

    def _compute_result(self) -> Any:
        # Placeholder for actual result computation logic
        return self.results_dict.get('result', None)

    def __str__(self) -> str:
        return f"MetricResult(name={self.metric_name}, params={self.metric_params}, result={self.result})"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        return cls(metric_name=metric_name, metric_params=metric_params, results_dict=results_dict)
