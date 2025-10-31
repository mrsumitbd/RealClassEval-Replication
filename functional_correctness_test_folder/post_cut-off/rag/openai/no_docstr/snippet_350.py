
import time
from collections import OrderedDict
from typing import Dict, List


class StartupProfiler:
    """Detailed startup profiling with bottleneck identification."""

    def __init__(self) -> None:
        """Initialize the profiler."""
        self._start_time: float = time.perf_counter()
        self._checkpoints: OrderedDict[str, float] = OrderedDict()
        self._last_time: float = self._start_time

    def checkpoint(self, name: str) -> None:
        """Record a timing checkpoint."""
        now = time.perf_counter()
        self._checkpoints[name] = now
        self._last_time = now

    def get_report(self) -> Dict[str, float]:
        """Get a performance report showing time deltas."""
        report: Dict[str, float] = {}
        prev_time = self._start_time
        for name, ts in self._checkpoints.items():
            report[name] = ts - prev_time
            prev_time = ts
        # Include total elapsed time
        report["total"] = time.perf_counter() - self._start_time
        return report

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        """Analyze the report and identify performance bottlenecks."""
        # Exclude the total key
        items = [(k, v) for k, v in report.items() if k != "total"]
        # Sort by descending time
        items.sort(key=lambda x: x[1], reverse=True)
        # Return names of checkpoints that exceed 10% of total time
        total = report.get("total", 0)
        bottlenecks = [name for name,
                       dur in items if total > 0 and dur / total > 0.10]
        return bottlenecks
