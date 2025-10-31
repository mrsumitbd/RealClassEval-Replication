
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        self.checkpoints: Dict[str, float] = {}
        self.start_time: float = time.time()

    def checkpoint(self, name: str):
        self.checkpoints[name] = time.time() - self.start_time

    def get_report(self) -> Dict[str, float]:
        return self.checkpoints

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        if not report:
            return []

        sorted_checkpoints = sorted(
            report.items(), key=lambda x: x[1], reverse=True)
        max_time = sorted_checkpoints[0][1]
        threshold = max_time * 0.8  # Consider bottlenecks as 80% of the max time

        bottlenecks = [
            name for name, t in sorted_checkpoints
            if t >= threshold
        ]
        return bottlenecks
