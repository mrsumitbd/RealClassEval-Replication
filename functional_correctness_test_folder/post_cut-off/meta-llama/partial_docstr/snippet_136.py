
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MetricResult:
    name: str = field(init=True)
    params: Dict[str, Any] = field(init=True)
    result: Any = field(init=True)

    def __str__(self) -> str:
        return f"Metric '{self.name}' with params {self.params}: {self.result}"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        result = results_dict.get('result', results_dict.get('value'))
        return cls(name=metric_name, params=metric_params, result=result)
