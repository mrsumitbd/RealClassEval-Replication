
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self.checkpoints = {}
        self.start_time = time.time()

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        current_time = time.time()
        self.checkpoints[name] = current_time

    def get_report(self) -> Dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report = {}
        previous_time = self.start_time
        for name, timestamp in self.checkpoints.items():
            report[name] = timestamp - previous_time
            previous_time = timestamp
        return report

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        average_time = sum(report.values()) / len(report)
        return [name for name, time_taken in report.items() if time_taken > average_time]


# Example usage:
if __name__ == "__main__":
    profiler = StartupProfiler()
    profiler.checkpoint('init_start')
    time.sleep(1)  # Simulating some work
    profiler.checkpoint('init_end')
    time.sleep(2)  # Simulating some more work
    profiler.checkpoint('loading_start')
    time.sleep(1)  # Simulating some work
    profiler.checkpoint('loading_end')

    report = profiler.get_report()
    print("Performance Report:")
    for name, time_taken in report.items():
        print(f"{name}: {time_taken} seconds")

    bottlenecks = profiler.analyze_bottlenecks(report)
    print("\nIdentified Bottlenecks:")
    for bottleneck in bottlenecks:
        print(bottleneck)
