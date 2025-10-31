from time import perf_counter
from typing import List, Tuple, Dict
import threading


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        self._lock = threading.Lock()
        self._checkpoints: List[Tuple[str, float]] = []
        start_time = perf_counter()
        self._checkpoints.append(('start', start_time))

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        now = perf_counter()
        with self._lock:
            self._checkpoints.append((name, now))

    def get_report(self) -> dict[str, float]:
        '''Get a performance report showing time deltas.'''
        with self._lock:
            cps = list(self._checkpoints)

        report: Dict[str, float] = {}
        if len(cps) < 2:
            report['total'] = 0.0
            return report

        name_counts: Dict[str, int] = {}
        total = 0.0
        for i in range(1, len(cps)):
            prev_name, prev_t = cps[i - 1]
            name, t = cps[i]
            delta = max(0.0, t - prev_t)
            total += delta

            count = name_counts.get(name, 0)
            safe_name = name if count == 0 else f'{name}#{count + 1}'
            name_counts[name] = count + 1

            report[safe_name] = delta

        report['total'] = total
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []
        durations = {k: v for k, v in report.items() if k != 'total'}
        if not durations:
            return []

        total = report.get('total', sum(durations.values()))
        if total <= 0:
            # Return top entries by absolute time (if any are > 0), else empty
            top = [k for k, v in sorted(
                durations.items(), key=lambda x: x[1], reverse=True) if v > 0]
            return top[:3]

        threshold = 0.2 * total
        bottlenecks = [k for k, v in durations.items() if v >= threshold]
        if bottlenecks:
            bottlenecks.sort(key=lambda k: durations[k], reverse=True)
            return bottlenecks

        # If nothing exceeds threshold, return top 3 contributors
        top = [k for k, _ in sorted(
            durations.items(), key=lambda x: x[1], reverse=True)]
        return top[:3]
