import time
from typing import List, Dict


class StartupProfiler:

    def __init__(self):
        self._start = time.perf_counter()
        self._checkpoints: list[tuple[str, float]] = []

    def checkpoint(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Checkpoint name must be a non-empty string.")
        self._checkpoints.append((name.strip(), time.perf_counter()))

    def get_report(self) -> dict[str, float]:
        report: Dict[str, float] = {}
        prev_time = self._start
        name_counts: Dict[str, int] = {}
        last_time = self._start

        for raw_name, t in self._checkpoints:
            duration = t - prev_time
            name_counts[raw_name] = name_counts.get(raw_name, 0) + 1
            name = raw_name if name_counts[
                raw_name] == 1 else f"{raw_name} ({name_counts[raw_name]})"
            report[name] = duration
            prev_time = t
            last_time = t

        total = max(0.0, last_time - self._start)
        report["total"] = total
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        keys = [k for k in report.keys() if k != "total"]
        return sorted(keys, key=lambda k: report[k], reverse=True)
