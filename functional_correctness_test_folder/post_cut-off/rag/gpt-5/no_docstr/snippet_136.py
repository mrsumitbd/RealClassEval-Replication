from dataclasses import dataclass
from typing import Any, Dict, Union


Number = Union[int, float]


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
    result: Number

    def __str__(self) -> str:
        '''
        Return a string representation of the MetricResult, including the name and the result.
        Returns
        -------
        str
            A string representation of the MetricResult.
        '''
        return f"MetricResult(name={self.name}, result={self.result})"

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
        def is_number(x: Any) -> bool:
            return isinstance(x, (int, float)) and not isinstance(x, bool)

        def extract_number(obj: Any) -> Union[Number, None]:
            if is_number(obj):
                return obj
            if isinstance(obj, dict):
                # Common keys that might hold the numeric result
                for key in ('result', 'value', 'score'):
                    val = obj.get(key)
                    if is_number(val):
                        return val
            return None

        value = None

        # 1) Direct key match
        if metric_name in results_dict:
            value = extract_number(results_dict[metric_name])

        # 2) Common generic keys at top-level
        if value is None:
            for key in ('result', 'value', 'score'):
                if key in results_dict:
                    value = extract_number(results_dict[key])
                    if value is not None:
                        break

        # 3) Single-item dict with numeric value
        if value is None and len(results_dict) == 1:
            only_val = next(iter(results_dict.values()))
            value = extract_number(only_val)

        # 4) Fallback: scan top-level values for first numeric
        if value is None:
            for v in results_dict.values():
                value = extract_number(v)
                if value is not None:
                    break

        if value is None:
            raise ValueError(
                "Could not determine a numeric result from results_dict")

        return cls(name=metric_name, params=dict(metric_params or {}), result=value)
