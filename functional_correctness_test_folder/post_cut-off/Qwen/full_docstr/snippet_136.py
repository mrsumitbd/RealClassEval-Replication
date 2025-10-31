
from dataclasses import dataclass
from typing import Dict, Any, Union


@dataclass
class MetricResult:
    name: str
    params: Dict[str, Any]
    result: Union[float, int]

    def __str__(self) -> str:
        return f"MetricResult(name={self.name}, result={self.result})"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        result_value = results_dict.get('result')
        return cls(name=metric_name, params=metric_params, result=result_value)
