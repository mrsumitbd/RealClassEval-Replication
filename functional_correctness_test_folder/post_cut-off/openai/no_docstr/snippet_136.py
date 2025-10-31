
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    results: Dict[str, Any]

    def __str__(self) -> str:
        """Return a human‑readable representation of the metric result."""
        params_str = ", ".join(
            f"{k}={v!r}" for k, v in sorted(self.metric_params.items()))
        results_str = ", ".join(
            f"{k}={v!r}" for k, v in sorted(self.results.items()))
        return f"{self.metric_name}({params_str}) -> {{{results_str}}}"

    @classmethod
    def from_results_dict(
        cls,
        metric_name: str,
        metric_params: Dict[str, Any],
        results_dict: Dict[str, Any],
    ) -> "MetricResult":
        """Create a MetricResult instance from the given dictionaries."""
        return cls(metric_name=metric_name, metric_params=metric_params, results=results_dict)
