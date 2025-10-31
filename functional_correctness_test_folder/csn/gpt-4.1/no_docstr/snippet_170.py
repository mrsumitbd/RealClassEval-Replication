
class MetricsDAO:
    def __init__(self):
        self._data = {}

    def get(self, run_id, metric_id):
        return self._data.get(run_id, {}).get(metric_id, None)

    def delete(self, run_id):
        if run_id in self._data:
            del self._data[run_id]
