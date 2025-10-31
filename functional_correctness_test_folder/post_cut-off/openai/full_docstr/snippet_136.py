
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
        # Try to find the result in the dictionary.
        # Common patterns: a key named "result" or the metric name itself.
        if "result" in results_dict:
            result_value = results_dict["result"]
        elif metric_name in results_dict:
            result_value = results_dict[metric_name]
        else:
            # If no obvious key, raise an informative error.
            raise ValueError(
                f"Could not find result for metric '{metric_name}' in results_dict: {results_dict}"
            )

        return cls(name=metric_name, params=metric_params, result=result_value)
