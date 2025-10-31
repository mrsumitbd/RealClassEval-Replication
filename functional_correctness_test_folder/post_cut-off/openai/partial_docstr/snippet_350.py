
import time
from typing import Dict, List


class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        # Record the absolute start time of the profiling session
        self._start_time: float = time.perf_counter()
        # Ordered list of checkpoint names
        self._checkpoints: List[str] = []
        # Mapping from checkpoint name to its timestamp
        self._times: Dict[str, float] = {}

    def checkpoint(self, name: str):
        """Record a checkpoint with the given name."""
        if name in self._times:
            raise ValueError(f"Checkpoint '{name}' already recorded.")
        self._checkpoints.append(name)
        self._times[name] = time.perf_counter()

    def get_report(self) -> Dict[str, float]:
        """
        Return a dictionary mapping each checkpoint name to the elapsed
        time (in seconds) since the previous checkpoint (or since start
        for the first checkpoint).
        """
        report: Dict[str, float] = {}
        prev_time = self._start_time
        for name in self._checkpoints:
            curr_time = self._times[name]
            report[name] = curr_time - prev_time
            prev_time = curr_time
        return report

    def analyze_bottlenecks(self, report: Dict[str, float]) -> List[str]:
        """
        Return a list of checkpoint names sorted by descending duration.
        """
        # Sort by duration descending; if equal, preserve original order
        sorted_items = sorted(
            report.items(), key=lambda kv: kv[1], reverse=True)
        return [name for name, _ in sorted_items]
