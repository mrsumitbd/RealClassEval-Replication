
import time


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self.checkpoints = {}
        self.start_time = time.time()

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        self.checkpoints[name] = time.time() - self.start_time

    def get_report(self) -> dict[str, float]:
        '''Get a performance report showing time deltas.'''
        report = {}
        previous_time = 0.0
        for name in sorted(self.checkpoints.keys()):
            current_time = self.checkpoints[name]
            report[name] = current_time - previous_time
            previous_time = current_time
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        threshold = 0.1  # Define a threshold for what constitutes a bottleneck
        bottlenecks = [name for name, duration in report.items()
                       if duration > threshold]
        return bottlenecks
