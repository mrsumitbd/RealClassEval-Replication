
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
        # Try to locate the result value in the dictionary.
        if "result" in results_dict:
            result_value = results_dict["result"]
        elif metric_name in results_dict:
            result_value = results_dict[metric_name]
        else:
            # If no obvious key, fall back to the first numeric value found.
            numeric_candidates = [
                v for v in results_dict.values() if isinstance(v, (int, float))
            ]
            if numeric_candidates:
                result_value = numeric_candidates[0]
            else:
                raise ValueError(
                    f"Could not find a numeric result for metric '{metric_name}' "
                    f"in the provided results dictionary."
                )

        return cls(name=metric_name, params=metric_params, result=result_value)
