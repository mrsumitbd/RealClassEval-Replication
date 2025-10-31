
import datetime
from typing import Dict, List, Any


class NotFoundError(Exception):
    """Raised when a requested metric or run is not found."""
    pass


class MetricsDAO:
    """
    Interface for accessing Sacred metrics.
    Issue: https://github.com/chovanecm/sacredboard/issues/58
    Extended because of: https://github.com/chovanecm/sacredboard/issues/66
    """

    def __init__(self):
        # Storage format: {run_id: {metric_id: metric_dict}}
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def add_metric(
        self,
        run_id: str,
        metric_id: str,
        name: str,
        steps: List[int],
        timestamps: List[datetime.datetime],
        values: List[float],
    ) -> None:
        """
        Helper method to add a metric to the store.
        """
        if run_id not in self._store:
            self._store[run_id] = {}
        self._store[run_id][metric_id] = {
            "steps": steps,
            "timestamps": timestamps,
            "values": values,
            "name": name,
            "metric_id": metric_id,
            "run_id": run_id,
        }

    def get(self, run_id: str, metric_id: str) -> Dict[str, Any]:
        """
        Read a metric of the given id and run.
        The returned object has the following format (timestamps are datetime
         objects).
        .. code::
            {"steps": [0,1,20,40,...],
            "timestamps": [timestamp1,timestamp2,timestamp3,...],
            "values": [0,1 2,3,4,5,6,...],
            "name": "name of the metric",
            "metric_id": "metric_id",
            "run_id": "run_id"}
        :param run_id: ID of the Run that the metric belongs to.
        :param metric_id: The ID fo the metric.
        :return: The whole metric as specified.
        :raise NotFoundError
        """
        run_metrics = self._store.get(run_id)
        if not run_metrics:
            raise NotFoundError(f"Run {run_id} not found.")
        metric = run_metrics.get(metric_id)
        if not metric:
            raise NotFoundError(
                f"Metric {metric_id} not found for run {run_id}.")
        return metric

    def delete(self, run_id: str) -> None:
        """
        Delete all metrics belonging to the given run.
        :param run_id: ID of the Run that the metric belongs to.
        """
        if run_id in self._store:
            del self._store[run_id]
