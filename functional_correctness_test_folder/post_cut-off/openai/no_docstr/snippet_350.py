
import time
from typing import Dict, List


class StartupProfiler:
    def __init__(self):
        # Stores the timestamp of each checkpoint
        self._timestamps: Dict[str, float] = {}
        # Stores the elapsed time between the previous checkpoint and this one
        self._durations: Dict[str, float] = {}
        # Timestamp of the last checkpoint
        self._last_time: float | None = None

    def checkpoint(self, name: str):
        """Record a checkpoint with the given name."""
        now = time.perf_counter()
        if self._last_time is not None:
            # Duration since the previous checkpoint
            self._durations[name] = now - self._last_time
        else:
            # First checkpoint: no duration to record
            self._durations[name] = 0.0
        self._timestamps[name] = now
        self._last_time = now

    def get_report(self) -> Dict[str, float]:
        """Return a dictionary mapping checkpoint names to elapsed times."""
        return dict(self._durations)

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        """
        Return a list of checkpoint names sorted by descending elapsed time.
        This helps identify the slowest parts of the startup sequence.
        """
        return sorted(report, key=report.get, reverse=True)
