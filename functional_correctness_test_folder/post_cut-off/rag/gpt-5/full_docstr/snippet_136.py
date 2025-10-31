from dataclasses import dataclass
from typing import Any, Dict, Union


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
        if not isinstance(results_dict, dict):
            raise TypeError("results_dict must be a dictionary")

        def is_number(x: Any) -> bool:
            return isinstance(x, (int, float)) and not isinstance(x, bool)

        candidate_keys = [metric_name, 'result', 'value', 'score']
        result_value: Union[float, int, None] = None

        for key in candidate_keys:
            if key in results_dict and is_number(results_dict[key]):
                result_value = results_dict[key]
                break

        if result_value is None:
            for key in ['mean', 'avg', 'average', 'median', f'{metric_name}_mean']:
                if key in results_dict and is_number(results_dict[key]):
                    result_value = results_dict[key]
                    break

        if result_value is None:
            numeric_values = [(k, v)
                              for k, v in results_dict.items() if is_number(v)]
            if len(numeric_values) == 1:
                result_value = numeric_values[0][1]

        if result_value is None:
            raise ValueError(
                "Could not determine numeric result from results_dict")

        return cls(name=metric_name, params=dict(metric_params) if metric_params is not None else {}, result=result_value)
