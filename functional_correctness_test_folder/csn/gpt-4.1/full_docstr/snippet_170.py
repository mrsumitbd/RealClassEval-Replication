
from datetime import datetime


class NotFoundError(Exception):
    pass


class MetricsDAO:
    '''
    Interface for accessing Sacred metrics.
    Issue: https://github.com/chovanecm/sacredboard/issues/58
    Extended because of: https://github.com/chovanecm/sacredboard/issues/66
    '''

    def __init__(self):
        # Storage format: {run_id: {metric_id: metric_dict}}
        self._storage = {}

    def get(self, run_id, metric_id):
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
        if run_id not in self._storage or metric_id not in self._storage[run_id]:
            raise NotFoundError(
                f"Metric '{metric_id}' for run '{run_id}' not found.")
        return self._storage[run_id][metric_id]

    def delete(self, run_id):
        '''
        Delete all metrics belonging to the given run.
        :param run_id: ID of the Run that the metric belongs to.
        '''
        if run_id in self._storage:
            del self._storage[run_id]
