
import time
from typing import Dict, List


class StartupProfiler:
    """Detailed startup profiling with bottleneck identification."""

    def __init__(self) -> None:
        """Initialize the profiler."""
        self._start_time: float = time.perf_counter()
        self._prev_time: float = self._start_time
        self._deltas: Dict[str, float] = {}

    def checkpoint(self, name: str) -> None:
        """Record a timing checkpoint."""
        now = time.perf_counter()
        delta = now - self._prev_time
        self._deltas[name] = delta
        self._prev_time = now

    def get_report(self) -> Dict[str, float]:
        """Get a performance report showing time deltas."""
        return dict(self._deltas)

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        """Analyze the report and identify performance bottlenecks."""
        # Return the names sorted by descending time; optionally filter
        # by a threshold (e.g., > 0.1s) or top N.
        threshold = 0.1  # seconds
        bottlenecks = [name for name, t in report.items() if t >= threshold]
        # Sort by time descending
        bottlenecks.sort(key=lambda n: report[n], reverse=True)
        return bottlenecks
