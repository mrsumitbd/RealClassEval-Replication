
class MetricsDAO:
    def __init__(self):
        # In‑memory storage: {run_id: {metric_id: value}}
        self._store = {}

    def get(self, run_id, metric_id):
        """Return the metric value for the given run_id and metric_id, or None if not found."""
        return self._store.get(run_id, {}).get(metric_id)

    def delete(self, run_id):
        """Remove all metrics associated with the given run_id."""
        self._store.pop(run_id, None)
