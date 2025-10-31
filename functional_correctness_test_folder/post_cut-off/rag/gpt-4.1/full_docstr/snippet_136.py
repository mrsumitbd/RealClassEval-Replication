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
        return f"MetricResult(name={self.name!r}, result={self.result!r}, params={self.params!r})"

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
        # Try to get the result from the results_dict using the metric_name as key
        if metric_name in results_dict:
            result = results_dict[metric_name]
        elif "result" in results_dict:
            result = results_dict["result"]
        else:
            raise ValueError(
                f"Result for metric '{metric_name}' not found in results_dict.")
        return cls(name=metric_name, params=metric_params, result=result)
