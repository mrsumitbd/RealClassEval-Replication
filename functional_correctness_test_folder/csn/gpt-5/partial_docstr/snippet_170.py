import threading
import copy


class MetricsDAO:
    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()

    def get(self, run_id, metric_id):
        if run_id is None:
            raise ValueError("run_id must not be None")
        if metric_id is None:
            raise ValueError("metric_id must not be None")
        with self._lock:
            run_metrics = self._data.get(run_id, {})
            value = run_metrics.get(metric_id)
            return copy.deepcopy(value)

    def delete(self, run_id):
        '''
        Delete all metrics belonging to the given run.
        :param run_id: ID of the Run that the metric belongs to.
        '''
        if run_id is None:
            raise ValueError("run_id must not be None")
        with self._lock:
            if run_id in self._data:
                del self._data[run_id]
                return True
            return False
