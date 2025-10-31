
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
        # The raw results dictionary may contain the result under a key named
        # 'result', or it may be the result itself.  Handle both cases.
        if isinstance(results_dict, dict) and "result" in results_dict:
            result_value = results_dict["result"]
        else:
            result_value = results_dict

        return cls(name=metric_name, params=metric_params, result=result_value)
