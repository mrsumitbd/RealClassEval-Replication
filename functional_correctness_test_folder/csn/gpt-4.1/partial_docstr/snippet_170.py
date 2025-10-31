
class MetricsDAO:
    def __init__(self):
        # Storage format: {run_id: {metric_id: metric_value}}
        self._storage = {}

    def get(self, run_id, metric_id):
        return self._storage.get(run_id, {}).get(metric_id, None)

    def delete(self, run_id):
        if run_id in self._storage:
            del self._storage[run_id]
