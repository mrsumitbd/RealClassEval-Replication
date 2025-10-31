
from datetime import datetime
from typing import List, Dict, Any
from collections.abc import Iterable


class NotFoundError(Exception):
    pass


class MetricsDAO:
    '''
    Interface for accessing Sacred metrics.
    Issue: https://github.com/chovanecm/sacredboard/issues/58
    Extended because of: https://github.com/chovanecm/sacredboard/issues/66
    '''

    def __init__(self):
        self.metrics_store = {}

    def get(self, run_id: str, metric_id: str) -> Dict[str, Any]:
        '''
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
        '''
        if run_id not in self.metrics_store or metric_id not in self.metrics_store[run_id]:
            raise NotFoundError(
                f"Metric with ID {metric_id} not found for run {run_id}.")
        return self.metrics_store[run_id][metric_id]

    def delete(self, run_id: str):
        '''
        Delete all metrics belonging to the given run.
        :param run_id: ID of the Run that the metric belongs to.
        '''
        if run_id in self.metrics_store:
            del self.metrics_store[run_id]

    def add_metric(self, run_id: str, metric_id: str, steps: List[int], timestamps: List[datetime], values: List[float], name: str):
        if run_id not in self.metrics_store:
            self.metrics_store[run_id] = {}
        self.metrics_store[run_id][metric_id] = {
            "steps": steps,
            "timestamps": timestamps,
            "values": values,
            "name": name,
            "metric_id": metric_id,
            "run_id": run_id
        }
