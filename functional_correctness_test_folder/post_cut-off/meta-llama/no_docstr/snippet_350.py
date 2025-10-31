
import time
from typing import Dict, List


class StartupProfiler:

    def __init__(self):
        self.checkpoints = {}
        self.start_time = time.time()

    def checkpoint(self, name: str):
        current_time = time.time()
        self.checkpoints[name] = current_time - self.start_time

    def get_report(self) -> Dict[str, float]:
        return self.checkpoints.copy()

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        sorted_report = sorted(
            report.items(), key=lambda x: x[1], reverse=True)
        bottlenecks = [name for name, duration in sorted_report if duration > (
            sorted_report[0][1] * 0.1 if sorted_report else 0)]
        return bottlenecks


# Example usage:
if __name__ == "__main__":
    profiler = StartupProfiler()
    profiler.checkpoint("init_start")
    time.sleep(1)
    profiler.checkpoint("db_connected")
    time.sleep(2)
    profiler.checkpoint("api_initialized")
    report = profiler.get_report()
    print("Report:", report)
    bottlenecks = profiler.analyze_bottlenecks(report)
    print("Bottlenecks:", bottlenecks)
