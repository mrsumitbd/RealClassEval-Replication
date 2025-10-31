
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
        # Initialize an in-memory data store for demonstration purposes.
        # In a real application, this would be replaced with a database connection.
        self.metrics = {}

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
        if run_id not in self.metrics or metric_id not in self.metrics[run_id]:
            raise NotFoundError(
                f"Metric {metric_id} not found for run {run_id}")

        metric = self.metrics[run_id][metric_id]
        return {
            "steps": metric["steps"],
            "timestamps": [datetime.fromtimestamp(ts) for ts in metric["timestamps"]],
            "values": metric["values"],
            "name": metric["name"],
            "metric_id": metric_id,
            "run_id": run_id
        }

    def delete(self, run_id):
        '''
        Delete all metrics belonging to the given run.
        :param run_id: ID of the Run that the metric belongs to.
        '''
        if run_id in self.metrics:
            del self.metrics[run_id]

    def add_metric(self, run_id, metric_id, name, steps, timestamps, values):
        # Helper method to add a metric for testing purposes.
        if run_id not in self.metrics:
            self.metrics[run_id] = {}

        self.metrics[run_id][metric_id] = {
            "name": name,
            "steps": steps,
            "timestamps": timestamps,
            "values": values
        }


# Example usage:
if __name__ == "__main__":
    dao = MetricsDAO()
    dao.add_metric("run1", "metric1", "Metric 1", [0, 1, 2], [
                   1643723400, 1643723410, 1643723420], [10, 20, 30])
    print(dao.get("run1", "metric1"))
    dao.delete("run1")
    try:
        print(dao.get("run1", "metric1"))
    except NotFoundError as e:
        print(e)
