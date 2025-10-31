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
        if not isinstance(results_dict, dict):
            raise TypeError("results_dict must be a dictionary")

        # Priority keys commonly used for metric values
        priority_keys = (
            "result",
            "score",
            "value",
            metric_name,
            "metric",
            "accuracy",
            "f1",
            "precision",
            "recall",
            "mse",
            "rmse",
            "mae",
            "map",
            "ndcg",
            "auc",
        )

        for key in priority_keys:
            if key in results_dict and isinstance(results_dict[key], (int, float)):
                return cls(name=metric_name, params=metric_params, result=results_dict[key])

        numeric_items = [(k, v) for k, v in results_dict.items()
                         if isinstance(v, (int, float))]
        if len(numeric_items) == 1:
            return cls(name=metric_name, params=metric_params, result=numeric_items[0][1])

        if len(numeric_items) == 0:
            raise ValueError("No numeric metric result found in results_dict")

        raise ValueError(
            "Multiple numeric values found in results_dict; cannot determine the metric result unambiguously")
