from typing import Any, Dict
from dataclasses import dataclass

@dataclass
class MetricResult:
    """
    A class to store the results of a metric.

    Parameters
    ----------
    name : str
        The name of the metric.
    params : Dict[str, Any]
        The parameters of the metric.
    result : float | int
        The result of the metric.
    """
    name: str
    params: Dict[str, Any]
    result: float | int

    def __str__(self) -> str:
        """
        Return a string representation of the MetricResult, including the name and the result.

        Returns
        -------
        str
            A string representation of the MetricResult.
        """
        return f'{self.name}: {self.result}'

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        """
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
        """
        assert metric_name in results_dict, f'Metric name {metric_name} not found in raw results'
        result = results_dict[metric_name]
        assert isinstance(result, (float, int)), f'Result for metric {metric_name} is not a float or int'
        return cls(metric_name, metric_params, result)