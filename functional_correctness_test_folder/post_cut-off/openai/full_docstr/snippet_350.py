
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self._checkpoints: List[tuple[str, float]] = []

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        self._checkpoints.append((name, time.perf_counter()))

    def get_report(self) -> Dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report: Dict[str, float] = {}
        if not self._checkpoints:
            return report

        # Compute delta from previous checkpoint
        prev_time = self._checkpoints[0][1]
        for name, curr_time in self._checkpoints[1:]:
            delta = curr_time - prev_time
            report[name] = delta
            prev_time = curr_time

        # If only one checkpoint, report zero for that checkpoint
        if len(self._checkpoints) == 1:
            report[self._checkpoints[0][0]] = 0.0

        return report

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []

        total_time = sum(report.values())
        if total_time == 0:
            return []

        # Define bottleneck as >10% of total time
        threshold = 0.10 * total_time
        bottlenecks = [name for name, t in report.items() if t >= threshold]

        # Sort by descending time
        bottlenecks.sort(key=lambda n: report[n], reverse=True)
        return bottlenecks
