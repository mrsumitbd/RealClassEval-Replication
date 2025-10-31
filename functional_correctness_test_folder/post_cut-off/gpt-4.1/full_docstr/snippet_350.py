
import time


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self._checkpoints = []
        self._times = []

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        now = time.perf_counter()
        self._checkpoints.append(name)
        self._times.append(now)

    def get_report(self) -> dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report = {}
        if len(self._checkpoints) < 2:
            return report
        for i in range(1, len(self._checkpoints)):
            delta = self._times[i] - self._times[i-1]
            key = f"{self._checkpoints[i-1]} -> {self._checkpoints[i]}"
            report[key] = delta
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []
        values = list(report.values())
        avg = sum(values) / len(values)
        threshold = max(avg * 1.5, max(values) * 0.7)
        bottlenecks = [k for k, v in report.items() if v >= threshold]
        return bottlenecks
