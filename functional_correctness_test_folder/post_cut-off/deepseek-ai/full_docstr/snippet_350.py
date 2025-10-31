
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self.checkpoints = {}
        self.start_time = time.time()
        self.last_checkpoint = self.start_time

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        current_time = time.time()
        self.checkpoints[name] = current_time - self.last_checkpoint
        self.last_checkpoint = current_time

    def get_report(self) -> Dict[str, float]:
        '''Get a performance report showing time deltas.'''
        return self.checkpoints.copy()

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []
        max_delta = max(report.values())
        return [name for name, delta in report.items() if delta == max_delta]
