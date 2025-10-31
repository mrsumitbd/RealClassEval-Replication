
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self._checkpoints: Dict[str, float] = {}
        self._start_time: float = time.perf_counter()
        self._checkpoints["start"] = self._start_time

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        self._checkpoints[name] = time.perf_counter()

    def get_report(self) -> Dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report = {}
        prev_time = self._start_time
        sorted_checkpoints = sorted(
            self._checkpoints.items(), key=lambda x: x[1])

        for name, current_time in sorted_checkpoints:
            report[name] = current_time - prev_time
            prev_time = current_time

        return report

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []

        max_duration = max(report.values())
        bottlenecks = [name for name, duration in report.items()
                       if duration == max_duration]

        return bottlenecks
