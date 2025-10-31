
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        self.checkpoints = {}
        self.start_time = time.time()

    def checkpoint(self, name: str):
        current_time = time.time()
        self.checkpoints[name] = current_time - self.start_time
        self.start_time = current_time

    def get_report(self) -> Dict[str, float]:
        return self.checkpoints.copy()

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        sorted_report = sorted(
            report.items(), key=lambda x: x[1], reverse=True)
        bottlenecks = [name for name,
                       duration in sorted_report if duration > 0.1]
        return bottlenecks


# Example usage:
if __name__ == "__main__":
    profiler = StartupProfiler()
    profiler.checkpoint('init_start')
    # Simulate some work
    time.sleep(0.05)
    profiler.checkpoint('init_end')
    # Simulate some more work
    time.sleep(0.2)
    profiler.checkpoint('loading_data')
    # Simulate some more work
    time.sleep(0.01)
    profiler.checkpoint('data_loaded')

    report = profiler.get_report()
    print("Report:", report)

    bottlenecks = profiler.analyze_bottlenecks(report)
    print("Bottlenecks:", bottlenecks)
