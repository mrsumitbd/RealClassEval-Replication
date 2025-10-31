
import time
from statistics import median
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        self._start_time = time.perf_counter()
        self._last_time = self._start_time
        self._durations: Dict[str, float] = {}

    def checkpoint(self, name: str):
        now = time.perf_counter()
        delta = now - self._last_time
        self._last_time = now
        if name in self._durations:
            self._durations[name] += delta
        else:
            self._durations[name] = delta

    def get_report(self) -> dict[str, float]:
        return dict(self._durations)

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        if not report:
            return []
        durations = list(report.values())
        total = sum(durations)
        if total <= 0:
            return []
        if len(durations) == 1:
            name, value = next(iter(report.items()))
            return [name] if value >= 0.1 else []

        med = median(durations)
        # Thresholds: absolute min, relative to median, relative to total
        abs_threshold = 0.05
        med_threshold = med * 2 if med > 0 else abs_threshold
        total_threshold = total * 0.2
        threshold = max(abs_threshold, med_threshold, total_threshold)

        candidates = [(name, dur)
                      for name, dur in report.items() if dur >= threshold]
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in candidates]
