from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import copy


@dataclass
class MetricResult:
    name: str
    params: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    details: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        '''
        Return a string representation of the MetricResult, including the name and the result.
        Returns
        -------
        str
            A string representation of the MetricResult.
        '''
        return f"{self.name}: {self.result}"

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        '''
        Create a MetricResult from a raw results dictionary.
        Parameters
        ----------
        metric_name : str
            The name of the metric.
        metric_params : Dict[str, Any]
            The parameters of the metric.
        results_dict : Dict[str, Any]
            The raw results dictionary.
        Returns
        -------
        MetricResult
            The MetricResult object.
        '''
        details = copy.deepcopy(
            results_dict) if results_dict is not None else {}
        if isinstance(results_dict, dict):
            result = results_dict.get(
                "result", results_dict.get("value", results_dict))
        else:
            result = results_dict
        return cls(name=metric_name, params=copy.deepcopy(metric_params) if metric_params else {}, result=result, details=details)
