
from dataclasses import dataclass
from typing import Dict, Any, Union


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
        return f"MetricResult(name='{self.name}', result={self.result})"

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
        # Try to get the result from the results_dict
        # Prefer 'result' key, else try the metric_name key, else raise error
        if 'result' in results_dict:
            result = results_dict['result']
        elif metric_name in results_dict:
            result = results_dict[metric_name]
        else:
            raise KeyError(
                f"Result not found in results_dict for metric '{metric_name}'")
        return cls(name=metric_name, params=metric_params, result=result)
