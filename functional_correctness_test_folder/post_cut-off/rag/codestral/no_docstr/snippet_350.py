
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
        for name, current_time in self.checkpoints.items():
            report[name] = current_time - prev_time
            prev_time = current_time
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []

        total_time = sum(report.values())
        bottlenecks = []

        for name, duration in report.items():
            percentage = (duration / total_time) * 100
            if percentage > 10:  # Consider as bottleneck if it takes more than 10% of total time
                bottlenecks.append(
                    f"{name}: {duration:.2f}s ({percentage:.1f}%)")

        return bottlenecks
