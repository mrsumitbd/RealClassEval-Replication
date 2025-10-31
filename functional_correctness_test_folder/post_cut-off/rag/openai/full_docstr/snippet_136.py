
from dataclasses import dataclass
from typing import Any, Dict, Union


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
    result: Union[float, int]

    def __str__(self) -> str:
        """
        Return a string representation of the MetricResult, including the name and the result.
        Returns
        -------
        str
            A string representation of the MetricResult.
        """
        return f"{self.name}: {self.result}"

    @classmethod
    def from_results_dict(
        cls,
        metric_name: str,
        metric_params: Dict[str, Any],
        results_dict: Dict[str, Any],
    ) -> "MetricResult":
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
        if metric_name not in results_dict:
            raise ValueError(
                f"Metric '{metric_name}' not found in results dictionary."
            )
        result = results_dict[metric_name]
        if not isinstance(result, (int, float)):
            raise TypeError(
                f"Result for metric '{metric_name}' must be int or float, got {type(result).__name__}."
            )
        return cls(name=metric_name, params=metric_params, result=result)
