import time
from typing import List, Dict


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self._checkpoints: List[tuple[str, float]] = []
        self._start_time = time.perf_counter()

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        now = time.perf_counter()
        self._checkpoints.append((name, now))

    def get_report(self) -> dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report: Dict[str, float] = {}
        prev_time = self._start_time
        for name, t in self._checkpoints:
            report[name] = t - prev_time
            prev_time = t
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []
        times = list(report.values())
        avg = sum(times) / len(times)
        threshold = max(avg * 2, max(times) * 0.8)
        bottlenecks = [name for name, t in report.items() if t >= threshold]
        return bottlenecks
