
import time


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        self._checkpoints = []
        self._times = []
        self._start_time = time.perf_counter()
        self._last_time = self._start_time

    def checkpoint(self, name: str):
        now = time.perf_counter()
        self._checkpoints.append(name)
        self._times.append(now - self._last_time)
        self._last_time = now

    def get_report(self) -> dict[str, float]:
        report = {}
        for name, duration in zip(self._checkpoints, self._times):
            report[name] = duration
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        if not report:
            return []
        durations = list(report.values())
        avg = sum(durations) / len(durations)
        threshold = max(avg * 1.5, max(durations) * 0.8)
        bottlenecks = [name for name, duration in report.items()
                       if duration >= threshold]
        return bottlenecks
