class StartupProfiler:
    '''Detailed startup profiling with bottleneck identification.'''

    def __init__(self):
        '''Initialize the profiler.'''
        import time
        self._time = time
        self._checkpoints: list[tuple[str, float]] = []
        self._start_time = self._time.perf_counter()
        self._checkpoints.append(("__start__", self._start_time))

    def checkpoint(self, name: str):
        '''Record a timing checkpoint.'''
        t = self._time.perf_counter()
        self._checkpoints.append((name, t))

    def get_report(self) -> dict[str, float]:
        '''Get a performance report showing time deltas.'''
        if len(self._checkpoints) < 2:
            return {}
        report: dict[str, float] = {}
        prev_time = self._checkpoints[0][1]
        for name, t in self._checkpoints[1:]:
            delta = t - prev_time
            key = name
            if key in report:
                i = 2
                while f"{name} ({i})" in report:
                    i += 1
                key = f"{name} ({i})"
            report[key] = delta
            prev_time = t
        total = sum(v for k, v in report.items())
        report["TOTAL"] = total
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        '''Analyze the report and identify performance bottlenecks.'''
        if not report:
            return []
        entries = [(k, v) for k, v in report.items() if k != "TOTAL"]
        if not entries:
            return []
        total = report.get("TOTAL", sum(v for _, v in entries))
        if total <= 0:
            total = sum(v for _, v in entries)
        durations = [v for _, v in entries]
        n = len(durations)
        mean = sum(durations) / n
        # Compute a simple population standard deviation
        var = sum((d - mean) ** 2 for d in durations) / n if n else 0.0
        std = var ** 0.5
        # Threshold: either significant fraction of total or notably above mean
        frac_threshold = 0.2 * total if total > 0 else mean
        sigma_threshold = mean + 0.5 * std
        threshold = max(frac_threshold, sigma_threshold)
        # Pick candidates above threshold; ensure at least top 3 if available
        sorted_entries = sorted(entries, key=lambda kv: kv[1], reverse=True)
        candidates = [kv for kv in sorted_entries if kv[1] >= threshold]
        if not candidates:
            candidates = sorted_entries[: min(3, len(sorted_entries))]
        result = []
        for name, dur in candidates:
            pct = (dur / total * 100.0) if total > 0 else 0.0
            result.append(f"{name}: {dur:.6f}s ({pct:.1f}%)")
        return result
