
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    value: Any

    def __str__(self) -> str:
        params_str = ', '.join(
            f'{key}={value}' for key, value in self.metric_params.items())
        return f'{self.metric_name}({params_str}): {self.value}'

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        value = results_dict.get(metric_name)
        if value is None:
            raise ValueError(
                f"Metric '{metric_name}' not found in results dictionary")
        return cls(metric_name, metric_params, value)
