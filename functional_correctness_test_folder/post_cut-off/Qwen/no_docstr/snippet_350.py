
import time


class StartupProfiler:

    def __init__(self):
        self.checkpoints = {}
        self.start_time = time.time()

    def checkpoint(self, name: str):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        self.checkpoints[name] = elapsed_time
        self.start_time = current_time

    def get_report(self) -> dict[str, float]:
        return self.checkpoints

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        sorted_report = sorted(
            report.items(), key=lambda item: item[1], reverse=True)
        # Assuming a bottleneck is any step taking more than 0.1 seconds
        return [name for name, _ in sorted_report if _ > 0.1]
