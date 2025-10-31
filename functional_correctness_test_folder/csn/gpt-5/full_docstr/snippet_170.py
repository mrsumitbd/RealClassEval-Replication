class NotFoundError(Exception):
    pass


class MetricsDAO:
    '''
    Interface for accessing Sacred metrics.
    Issue: https://github.com/chovanecm/sacredboard/issues/58
    Extended because of: https://github.com/chovanecm/sacredboard/issues/66
    '''

    def __init__(self, storage=None):
        self._storage = {}
        if storage:
            for run_id, metrics in storage.items():
                if isinstance(metrics, dict):
                    self._storage[run_id] = dict(metrics)
        try:
            from threading import RLock
            self._lock = RLock()
        except Exception:
            class DummyLock:
                def __enter__(self): return self
                def __exit__(self, *args): return False
            self._lock = DummyLock()

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
        with self._lock:
            run_metrics = self._storage.get(run_id)
            if not run_metrics or metric_id not in run_metrics:
                raise NotFoundError(
                    f"Metric '{metric_id}' for run '{run_id}' not found")
            metric = run_metrics[metric_id]
            result = {
                "steps": list(metric.get("steps", [])),
                "timestamps": list(metric.get("timestamps", [])),
                "values": list(metric.get("values", [])),
                "name": metric.get("name"),
                "metric_id": metric.get("metric_id", metric_id),
                "run_id": metric.get("run_id", run_id),
            }
            return result

    def delete(self, run_id):
        '''
        Delete all metrics belonging to the given run.
        :param run_id: ID of the Run that the metric belongs to.
        '''
        with self._lock:
            self._storage.pop(run_id, None)
