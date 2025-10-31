from dataclasses import dataclass
from typing import Any, Dict, Union
import numbers


@dataclass
class MetricResult:
    '''
    A class to store the results of a metric.
    Parameters
    ----------
    name : str
        The name of the metric.
    params : Dict[str, Any]
        The parameters of the metric.
    result : float | int
        The result of the metric.
    '''
    name: str
    params: Dict[str, Any]
    result: Union[float, int]

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
        if not isinstance(results_dict, dict):
            raise TypeError("results_dict must be a dictionary")

        # Prioritized keys to find the metric value
        candidate_keys = ("result", metric_name, "value", "score")
        value: Any = None
        for k in candidate_keys:
            if k in results_dict:
                value = results_dict[k]
                break

        # If not found by key, try to infer from the first numeric value present
        if value is None:
            numeric_items = [(k, v) for k, v in results_dict.items() if isinstance(v, numbers.Number) or (
                isinstance(v, str) and v.replace('.', '', 1).replace('-', '', 1).isdigit())]
            if len(numeric_items) == 1:
                value = numeric_items[0][1]

        if value is None:
            raise ValueError(
                "Could not determine result value from results_dict")

        # Coerce to int or float
        def coerce_result(v: Any) -> Union[int, float]:
            if isinstance(v, bool):
                return int(v)
            if isinstance(v, numbers.Integral):
                return int(v)
            if isinstance(v, numbers.Real):
                # Keep as int if it's exactly an integer value
                if float(v).is_integer():
                    return int(v)
                return float(v)
            if isinstance(v, str):
                try:
                    if '.' in v or 'e' in v.lower():
                        f = float(v)
                        if f.is_integer():
                            return int(f)
                        return f
                    return int(v)
                except ValueError:
                    pass
            raise TypeError(
                f"Result value {v!r} is not coercible to int or float")

        coerced_value = coerce_result(value)
        return cls(name=metric_name, params=dict(metric_params or {}), result=coerced_value)
