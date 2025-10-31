from dataclasses import dataclass
from typing import Any, Dict, Iterable


def _format_value(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:.6g}"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_format_value(x) for x in v) + "]"
    if isinstance(v, dict):
        items = ", ".join(f"{k}={_format_value(v[k])}" for k in sorted(v))
        return "{" + items + "}"
    return repr(v)


def _format_kv(d: Dict[str, Any]) -> str:
    if not d:
        return ""
    return ", ".join(f"{k}={_format_value(d[k])}" for k in sorted(d))


@dataclass
class MetricResult:
    metric_name: str
    metric_params: Dict[str, Any]
    results: Dict[str, Any]

    def __str__(self) -> str:
        params_str = _format_kv(self.metric_params)
        results_str = _format_kv(self.results)
        if params_str:
            header = f"{self.metric_name}({params_str})"
        else:
            header = self.metric_name
        if results_str:
            return f"{header}: {results_str}"
        return header

    @classmethod
    def from_results_dict(cls, metric_name: str, metric_params: Dict[str, Any], results_dict: Dict[str, Any]) -> 'MetricResult':
        metric_params = dict(metric_params or {})
        results_dict = dict(results_dict or {})
        return cls(metric_name=metric_name, metric_params=metric_params, results=results_dict)
