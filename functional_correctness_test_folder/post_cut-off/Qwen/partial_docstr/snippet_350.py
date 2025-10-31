
import time


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        self.checkpoints = {}
        self.start_time = time.time()

    def checkpoint(self, name: str):
        if name in self.checkpoints:
            raise ValueError(f"Checkpoint '{name}' already exists.")
        self.checkpoints[name] = time.time() - self.start_time

    def get_report(self) -> dict[str, float]:
        return self.checkpoints

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        sorted_report = sorted(
            report.items(), key=lambda item: item[1], reverse=True)
        max_time = sorted_report[0][1] if sorted_report else 0
        return [name for name, duration in sorted_report if duration == max_time]
