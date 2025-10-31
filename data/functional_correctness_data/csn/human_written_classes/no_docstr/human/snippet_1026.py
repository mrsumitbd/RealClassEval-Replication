class Metrics:

    def __init__(self, metrics):
        self._metrics = metrics

    def __len__(self):
        return len(self._metrics)

    def __getitem__(self, position):
        metric_values = self._metrics['result'][position]
        metric = None
        if metric_values is not None:
            metric = Metric(display_name=metric_values['displayName'])
        return metric

    def __str__(self):
        return str(self._metrics)