import time
import threading
from collections import defaultdict
from typing import List, Tuple, Dict


class StartupProfiler:
    """Detailed startup profiling with bottleneck identification."""

    def __init__(self):
        """Initialize the profiler."""
        self._lock = threading.Lock()
        self._start_time = time.perf_counter()
        self._checkpoints: List[Tuple[str, float]] = []
        self._name_counts: Dict[str, int] = defaultdict(int)

    def checkpoint(self, name: str):
        """Record a timing checkpoint."""
        now = time.perf_counter()
        with self._lock:
            self._name_counts[name] += 1
            count = self._name_counts[name]
            unique_name = name if count == 1 else f"{name}#{count}"
            self._checkpoints.append((unique_name, now))

    def get_report(self) -> dict[str, float]:
        """Get a performance report showing time deltas."""
        with self._lock:
            report: Dict[str, float] = {}
            prev = self._start_time
            for name, ts in self._checkpoints:
                report[name] = ts - prev
                prev = ts
            return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        """Analyze the report and identify performance bottlenecks."""
        if not report:
            return []
        total = sum(report.values())
        if total <= 0:
            # Degenerate case: all zeros
            return list(report.keys())

        mean = total / len(report)
        threshold = max(0.25 * total, 1.5 * mean)

        candidates = [name for name, dur in report.items() if dur >= threshold]
        if candidates:
            candidates.sort(key=lambda n: report[n], reverse=True)
            return candidates

        # If nothing crosses the threshold, return the single largest contributor.
        largest = max(report.items(), key=lambda kv: kv[1])[0]
        return [largest]
