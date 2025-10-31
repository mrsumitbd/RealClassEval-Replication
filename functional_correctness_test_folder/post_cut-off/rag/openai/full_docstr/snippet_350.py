
import time
from typing import Dict, List


class StartupProfiler:
    """Detailed startup profiling with bottleneck identification."""

    def __init__(self) -> None:
        """Initialize the profiler."""
        self._start_time: float = time.perf_counter()
        self._last_time: float = self._start_time
        self._checkpoints: Dict[str, float] = {}

    def checkpoint(self, name: str) -> None:
        """Record a timing checkpoint."""
        now = time.perf_counter()
        elapsed = now - self._last_time
        self._checkpoints[name] = elapsed
        self._last_time = now

    def get_report(self) -> Dict[str, float]:
        """Get a performance report showing time deltas."""
        return dict(self._checkpoints)

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        """
        Analyze the report and identify performance bottlenecks.

        Bottlenecks are defined as checkpoints whose elapsed time exceeds
        a configurable threshold (default 10 ms). The method returns a list
        of checkpoint names sorted by descending elapsed time.
        """
        threshold = 0.010  # 10 milliseconds
        bottlenecks = [
            name for name, elapsed in report.items() if elapsed > threshold
        ]
        bottlenecks.sort(key=lambda n: report[n], reverse=True)
        return bottlenecks
