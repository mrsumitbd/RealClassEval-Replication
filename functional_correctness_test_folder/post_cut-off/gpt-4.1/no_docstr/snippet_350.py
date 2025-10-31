
import time


class StartupProfiler:

    def __init__(self):
        self._checkpoints = []
        self._times = []
        self._started = False

    def checkpoint(self, name: str):
        now = time.perf_counter()
        if not self._started:
            self._started = True
            self._checkpoints.append(name)
            self._times.append(now)
        else:
            self._checkpoints.append(name)
            self._times.append(now)

    def get_report(self) -> dict[str, float]:
        if len(self._checkpoints) < 2:
            return {}
        report = {}
        for i in range(1, len(self._checkpoints)):
            prev = self._checkpoints[i-1]
            curr = self._checkpoints[i]
            duration = self._times[i] - self._times[i-1]
            report[f"{prev} -> {curr}"] = duration
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        if not report:
            return []
        if len(report) == 1:
            return list(report.keys())
        max_time = max(report.values())
        threshold = max_time * 0.9  # 90% of max time
        bottlenecks = [k for k, v in report.items() if v >= threshold]
        return bottlenecks
