
import time
from collections import defaultdict


class StartupProfiler:

    def __init__(self):
        self.checkpoints = defaultdict(list)
        self.start_time = time.time()

    def checkpoint(self, name: str):
        elapsed = time.time() - self.start_time
        self.checkpoints[name].append(elapsed)

    def get_report(self) -> dict[str, float]:
        report = {}
        for name, timings in self.checkpoints.items():
            if timings:
                report[name] = sum(timings) / len(timings)
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        if not report:
            return []
        max_time = max(report.values())
        bottlenecks = [name for name,
                       time in report.items() if time == max_time]
        return bottlenecks
