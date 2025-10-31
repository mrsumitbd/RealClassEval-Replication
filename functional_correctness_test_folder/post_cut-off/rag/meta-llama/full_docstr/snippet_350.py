
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self.start_time = time.time()
        self.checkpoints = {}

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        current_time = time.time()
        self.checkpoints[name] = current_time - self.start_time
        self.start_time = current_time

    def get_report(self) -> Dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report = {}
        prev_time = 0
        for name, timestamp in self.checkpoints.items():
            report[name] = timestamp - prev_time
            prev_time = timestamp
        return report

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        bottlenecks = []
        avg_time = sum(report.values()) / len(report)
        for name, time_taken in report.items():
            if time_taken > avg_time * 2:  # Consider it a bottleneck if it's more than twice the average
                bottlenecks.append(name)
        return bottlenecks
