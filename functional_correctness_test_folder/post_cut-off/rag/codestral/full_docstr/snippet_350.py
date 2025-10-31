
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
        prev_time = self.start_time
        for name, timestamp in self.checkpoints.items():
            report[name] = timestamp - prev_time
            prev_time = timestamp
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []

        total_time = sum(report.values())
        bottlenecks = []
        # Consider any step taking more than 20% of total time as a bottleneck
        threshold = total_time * 0.2

        for name, duration in report.items():
            if duration > threshold:
                bottlenecks.append(name)

        return bottlenecks
