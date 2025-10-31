
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self._checkpoints: Dict[str, float] = {}
        self._start_time: float = time.time()
        self._checkpoints["start"] = self._start_time

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        self._checkpoints[name] = time.time()

    def get_report(self) -> Dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report: Dict[str, float] = {}
        sorted_checkpoints = sorted(
            self._checkpoints.items(), key=lambda x: x[1])
        for i in range(1, len(sorted_checkpoints)):
            prev_name, prev_time = sorted_checkpoints[i-1]
            curr_name, curr_time = sorted_checkpoints[i]
            report[f"{prev_name} -> {curr_name}"] = curr_time - prev_time
        return report

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []
        max_delta = max(report.values())
        bottlenecks = [k for k, v in report.items() if v == max_delta]
        return bottlenecks
