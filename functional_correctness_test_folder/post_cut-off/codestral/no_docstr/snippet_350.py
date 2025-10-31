
import time


class StartupProfiler:

    def __init__(self):
        self.checkpoints = {}
        self.start_time = time.time()

    def checkpoint(self, name: str):
        self.checkpoints[name] = time.time() - self.start_time

    def get_report(self) -> dict[str, float]:
        return self.checkpoints

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        if not report:
            return []

        sorted_checkpoints = sorted(report.items(), key=lambda x: x[1])
        bottlenecks = [sorted_checkpoints[0][0]]

        for i in range(1, len(sorted_checkpoints)):
            if sorted_checkpoints[i][1] - sorted_checkpoints[i-1][1] < 0.1:
                bottlenecks.append(sorted_checkpoints[i][0])
            else:
                break

        return bottlenecks
