
class MetricsDAO:

    def __init__(self):
        self.metrics_store = {}

    def get(self, run_id, metric_id):
        if run_id in self.metrics_store and metric_id in self.metrics_store[run_id]:
            return self.metrics_store[run_id][metric_id]
        return None

    def delete(self, run_id):
        if run_id in self.metrics_store:
            del self.metrics_store[run_id]
