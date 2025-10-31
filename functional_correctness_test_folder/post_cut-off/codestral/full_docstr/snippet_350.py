
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
        previous_time = self.start_time
        for name, current_time in self.checkpoints.items():
            report[name] = current_time - previous_time
            previous_time = current_time
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []

        avg_time = sum(report.values()) / len(report)
        bottlenecks = [name for name,
                       delta in report.items() if delta > avg_time]
        return bottlenecks
