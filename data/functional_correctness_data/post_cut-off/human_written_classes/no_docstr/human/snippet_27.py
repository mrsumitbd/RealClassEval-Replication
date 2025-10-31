from datetime import datetime

class BenchmarkedModelStep:
    index: int
    recorded_at: datetime | None = None
    metrics: dict[str, float] = {}

    def __init__(self, index: int, metrics: dict[str, float] | None=None):
        self.index = index
        self.metrics = metrics if metrics is not None else {}

    def __str__(self):
        return f'{self.index} {self.metrics}'