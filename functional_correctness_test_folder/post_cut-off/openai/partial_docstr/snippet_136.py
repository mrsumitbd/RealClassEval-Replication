
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    result: Any

    def __str__(self) -> str:
        """
        Return a string representation of the MetricResult, including the name and the result.
        """
        return f"{self.metric_name}: {self.result}"

    @classmethod
    def from_results_dict(
        cls,
        metric_name: str,
        metric_params: Dict[str, Any],
        results_dict: Dict[str, Any],
    ) -> "MetricResult":
        """
        Create a MetricResult from a raw results dictionary.
        """
        # Prefer a 'result' key if present; otherwise use the whole dict
        result = results_dict.get("result", results_dict)
        return cls(metric_name=metric_name, metric_params=metric_params, result=result)
