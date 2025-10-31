import time
from typing import List, Tuple, Dict
import statistics


class StartupProfiler:
    """Detailed startup profiling with bottleneck identification."""

    def __init__(self):
        """Initialize the profiler."""
        self._start_ns: int = time.perf_counter_ns()
        self._events: List[Tuple[str, int]] = [("__start__", self._start_ns)]

    def checkpoint(self, name: str):
        """Record a timing checkpoint."""
        ts = time.perf_counter_ns()
        self._events.append((name if isinstance(name, str) else str(name), ts))

    def get_report(self) -> dict[str, float]:
        """Get a performance report showing time deltas."""
        if len(self._events) <= 1:
            return {}
        report: Dict[str, float] = {}
        prev_ts = self._events[0][1]
        used_names: Dict[str, int] = {}
        for name, ts in self._events[1:]:
            delta_s = (ts - prev_ts) / 1_000_000_000.0
            prev_ts = ts
            base = name.strip() or "checkpoint"
            count = used_names.get(base, 0) + 1
            used_names[base] = count
            key = base if count == 1 else f"{base}#{count}"
            report[key] = delta_s
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        """Analyze the report and identify performance bottlenecks."""
        if not report:
            return []
        durations = list(report.values())
        total = sum(durations)
        if total <= 0:
            return []
        items = sorted(report.items(), key=lambda kv: kv[1], reverse=True)

        # Small reports: return all significant segments
        if len(items) <= 3:
            return [k for k, v in items if v >= 0.01]

        mean = statistics.fmean(durations)
        stddev = statistics.pstdev(durations) if len(durations) > 1 else 0.0
        threshold = max(mean + stddev, 0.25 * total, 0.01)

        candidates = [k for k, v in items if v >= threshold]
        if not candidates:
            # Fallback: at least return the top segment if it’s meaningful
            top_name, top_val = items[0]
            return [top_name] if top_val >= max(0.02, 0.15 * total) else []
        return candidates
