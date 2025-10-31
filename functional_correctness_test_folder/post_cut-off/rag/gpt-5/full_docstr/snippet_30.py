from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Any, Dict, Optional, Mapping


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    count: int = 0
    successes: int = 0
    failures: int = 0

    total_duration_ms: int = 0
    min_duration_ms: Optional[int] = None
    max_duration_ms: Optional[int] = None

    first_timestamp_ms: Optional[int] = None
    last_timestamp_ms: Optional[int] = None

    # Generic aggregations
    sums: Dict[str, float] = field(default_factory=dict)
    true_counts: Dict[str, int] = field(default_factory=dict)

    def _entry_to_dict(self, entry: Any) -> Dict[str, Any]:
        if entry is None:
            return {}
        if isinstance(entry, Mapping):
            return dict(entry)
        if hasattr(entry, "to_dict") and callable(entry.to_dict):
            try:
                out = entry.to_dict()
                if isinstance(out, Mapping):
                    return dict(out)
            except Exception:
                pass
        if is_dataclass(entry):
            try:
                return asdict(entry)
            except Exception:
                pass
        # Fallback to object __dict__
        return dict(getattr(entry, "__dict__", {}))

    def _coerce_int_ms(self, value: Any) -> Optional[int]:
        try:
            if value is None:
                return None
            # Accept ints and floats; round to nearest millisecond
            if isinstance(value, (int, float)):
                return int(round(value))
            # Try to parse numeric strings
            if isinstance(value, str):
                v = float(value.strip())
                return int(round(v))
        except Exception:
            return None
        return None

    def _coerce_number(self, value: Any) -> Optional[float]:
        try:
            if isinstance(value, bool):
                # Treat booleans separately, not as numbers here
                return None
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                return float(value.strip())
        except Exception:
            return None
        return None

    def _update_min_max(self, v: int) -> None:
        if self.min_duration_ms is None or v < self.min_duration_ms:
            self.min_duration_ms = v
        if self.max_duration_ms is None or v > self.max_duration_ms:
            self.max_duration_ms = v

    def _update_first_last(self, start_ms: Optional[int], end_ms: Optional[int]) -> None:
        if start_ms is not None:
            if self.first_timestamp_ms is None or start_ms < self.first_timestamp_ms:
                self.first_timestamp_ms = start_ms
        if end_ms is not None:
            if self.last_timestamp_ms is None or end_ms > self.last_timestamp_ms:
                self.last_timestamp_ms = end_ms

    def _update_success_failure(self, payload: Dict[str, Any]) -> None:
        # Prefer explicit boolean 'success'
        if "success" in payload:
            val = payload.get("success")
            if isinstance(val, bool):
                if val:
                    self.successes += 1
                else:
                    self.failures += 1
                return
            # Sometimes success is "true"/"false"
            if isinstance(val, str):
                v = val.strip().lower()
                if v in {"true", "1", "yes"}:
                    self.successes += 1
                    return
                if v in {"false", "0", "no"}:
                    self.failures += 1
                    return

        # Check common status fields
        for key in ("status", "result", "outcome"):
            if key in payload and isinstance(payload[key], str):
                v = payload[key].strip().lower()
                success_tags = {"ok", "success", "succeeded",
                                "completed", "pass", "passed", "done"}
                failure_tags = {"fail", "failed", "error",
                                "errored", "aborted", "canceled", "cancelled"}
                if v in success_tags:
                    self.successes += 1
                    return
                if v in failure_tags:
                    self.failures += 1
                    return

        # Otherwise, we can't determine; do nothing.

    def _extract_duration_ms(self, payload: Dict[str, Any]) -> Optional[int]:
        # Prefer explicit duration fields with units
        if "duration_ms" in payload:
            return self._coerce_int_ms(payload.get("duration_ms"))

        if "duration_s" in payload:
            v = self._coerce_number(payload.get("duration_s"))
            if v is not None:
                return int(round(v * 1000.0))

        # Common alternates
        for k in ("elapsed_ms", "latency_ms", "time_ms"):
            if k in payload:
                v = self._coerce_int_ms(payload.get(k))
                if v is not None:
                    return v

        # Ambiguous names; only use if numeric and likely ms (heuristic)
        for k in ("duration", "elapsed", "latency", "time"):
            if k in payload:
                v = self._coerce_number(payload.get(k))
                if v is not None:
                    # Heuristic: if value seems like seconds (< 1e6), skip to avoid unit ambiguity
                    # Require a large value to treat as ms, or an integer clearly in ms range
                    if v >= 1e6:
                        return int(round(v))
        return None

    def _extract_start_end_ms(self, payload: Dict[str, Any]) -> tuple[Optional[int], Optional[int]]:
        # Start keys
        start_keys = (
            "start_ms",
            "started_at_ms",
            "timestamp_ms",
            "created_at_ms",
            "start_time_ms",
        )
        # End keys
        end_keys = (
            "end_ms",
            "ended_at_ms",
            "completed_at_ms",
            "stopped_at_ms",
            "finish_ms",
        )

        start_ms = None
        end_ms = None

        for k in start_keys:
            if k in payload:
                start_ms = self._coerce_int_ms(payload.get(k))
                if start_ms is not None:
                    break

        for k in end_keys:
            if k in payload:
                end_ms = self._coerce_int_ms(payload.get(k))
                if end_ms is not None:
                    break

        # Try to compute end if absent but have start + duration
        if end_ms is None and start_ms is not None:
            dur = self._extract_duration_ms(payload)
            if dur is not None:
                end_ms = start_ms + dur

        return start_ms, end_ms

    def add_entry(self, entry: 'UsageEntry') -> None:
        """Add an entry's statistics to this aggregate."""
        payload = self._entry_to_dict(entry)
        self.count += 1

        # Success/failure
        self._update_success_failure(payload)

        # Duration
        dur_ms = self._extract_duration_ms(payload)
        if dur_ms is not None:
            self.total_duration_ms += int(dur_ms)
            self._update_min_max(int(dur_ms))

        # First/last timestamps
        start_ms, end_ms = self._extract_start_end_ms(payload)
        self._update_first_last(start_ms, end_ms)

        # Generic numeric sums and boolean true-counts
        skip_keys = {
            "success",
            "status",
            "result",
            "outcome",
            "duration_ms",
            "duration_s",
            "elapsed_ms",
            "latency_ms",
            "time_ms",
            "duration",
            "elapsed",
            "latency",
            "time",
            "start_ms",
            "started_at_ms",
            "timestamp_ms",
            "created_at_ms",
            "start_time_ms",
            "end_ms",
            "ended_at_ms",
            "completed_at_ms",
            "stopped_at_ms",
            "finish_ms",
        }

        for k, v in payload.items():
            if k in skip_keys:
                continue
            if isinstance(v, bool):
                self.true_counts[k] = self.true_counts.get(
                    k, 0) + (1 if v else 0)
                continue
            num = self._coerce_number(v)
            if num is not None:
                self.sums[k] = self.sums.get(k, 0.0) + float(num)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        out: Dict[str, Any] = {
            "count": self.count,
            "successes": self.successes,
            "failures": self.failures,
            "total_duration_ms": self.total_duration_ms,
        }

        if self.min_duration_ms is not None:
            out["min_duration_ms"] = self.min_duration_ms
        if self.max_duration_ms is not None:
            out["max_duration_ms"] = self.max_duration_ms
        if self.first_timestamp_ms is not None:
            out["first_timestamp_ms"] = self.first_timestamp_ms
        if self.last_timestamp_ms is not None:
            out["last_timestamp_ms"] = self.last_timestamp_ms

        if self.sums:
            out["sums"] = dict(self.sums)
        if self.true_counts:
            out["true_counts"] = dict(self.true_counts)

        return out
