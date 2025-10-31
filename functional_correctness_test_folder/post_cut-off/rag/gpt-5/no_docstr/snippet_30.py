from __future__ import annotations

from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Any, Dict, Mapping, Optional
from datetime import datetime


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    # Counters
    count: int = 0

    # Numeric field aggregations
    _numeric_sums: Dict[str, float] = field(default_factory=dict)
    _numeric_mins: Dict[str, float] = field(default_factory=dict)
    _numeric_maxs: Dict[str, float] = field(default_factory=dict)
    _numeric_counts: Dict[str, int] = field(default_factory=dict)

    # Categorical field aggregations (value -> count)
    _categorical_counts: Dict[str, Dict[str, int]
                              ] = field(default_factory=dict)

    # Time range (epoch seconds)
    _first_timestamp: Optional[float] = None
    _last_timestamp: Optional[float] = None

    # Common timestamp field names to look for when tracking first/last timestamps
    _timestamp_keys: frozenset[str] = frozenset(
        {
            "timestamp",
            "time",
            "ts",
            "started_at",
            "ended_at",
            "created_at",
            "updated_at",
            "start_time",
            "end_time",
            "completed_at",
            "stopped_at",
            "finished_at",
        }
    )

    def _entry_to_mapping(self, entry: Any) -> Mapping[str, Any]:
        if entry is None:
            return {}
        if isinstance(entry, Mapping):
            return entry  # type: ignore[return-value]
        if is_dataclass(entry):
            return asdict(entry)
        if hasattr(entry, "to_dict") and callable(getattr(entry, "to_dict")):
            try:
                d = entry.to_dict()
                if isinstance(d, Mapping):
                    return d  # type: ignore[return-value]
            except Exception:
                pass
        if hasattr(entry, "__dict__"):
            return vars(entry)
        return {}

    def _maybe_to_epoch_seconds(self, value: Any) -> Optional[float]:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, datetime):
            try:
                return value.timestamp()
            except Exception:
                return None
        if isinstance(value, str):
            try:
                # Try ISO 8601
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return dt.timestamp()
            except Exception:
                return None
        return None

    def _update_timestamp_bounds(self, mapping: Mapping[str, Any]) -> None:
        for key in self._timestamp_keys:
            if key in mapping:
                ts = self._maybe_to_epoch_seconds(mapping[key])
                if ts is None:
                    continue
                if self._first_timestamp is None or ts < self._first_timestamp:
                    self._first_timestamp = ts
                if self._last_timestamp is None or ts > self._last_timestamp:
                    self._last_timestamp = ts

    def _is_numeric(self, value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def _add_numeric(self, key: str, value: float) -> None:
        self._numeric_sums[key] = self._numeric_sums.get(
            key, 0.0) + float(value)
        self._numeric_counts[key] = self._numeric_counts.get(key, 0) + 1
        if key not in self._numeric_mins or value < self._numeric_mins[key]:
            self._numeric_mins[key] = float(value)
        if key not in self._numeric_maxs or value > self._numeric_maxs[key]:
            self._numeric_maxs[key] = float(value)

    def _add_categorical(self, key: str, value: Any) -> None:
        if value is None:
            return
        value_key = str(value)
        inner = self._categorical_counts.setdefault(key, {})
        inner[value_key] = inner.get(value_key, 0) + 1

    def add_entry(self, entry: UsageEntry) -> None:
        """Add an entry's statistics to this aggregate."""
        mapping = self._entry_to_mapping(entry)
        if not mapping:
            self.count += 1  # still count the entry
            return

        self.count += 1
        self._update_timestamp_bounds(mapping)

        for key, value in mapping.items():
            if key.startswith("_"):
                continue
            if key in self._timestamp_keys:
                # Already processed as timestamp; skip from other aggregations
                continue
            if self._is_numeric(value):
                self._add_numeric(key, float(value))
            else:
                # Treat non-numeric scalars as categorical
                # Skip obvious non-scalar containers
                if isinstance(value, (list, tuple, set, dict)):
                    continue
                self._add_categorical(key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        numeric: Dict[str, Dict[str, Any]] = {}
        for key in self._numeric_sums:
            cnt = self._numeric_counts.get(key, 0)
            s = self._numeric_sums.get(key, 0.0)
            mn = self._numeric_mins.get(key, None)
            mx = self._numeric_maxs.get(key, None)
            avg = (s / cnt) if cnt > 0 else None
            numeric[key] = {
                "count": cnt,
                "sum": s,
                "min": mn,
                "max": mx,
                "avg": avg,
            }

        categorical: Dict[str, Dict[str, Any]] = {}
        for key, counts in self._categorical_counts.items():
            categorical[key] = {
                "counts": dict(counts),
                "unique": len(counts),
            }

        return {
            "count": self.count,
            "numeric": numeric,
            "categorical": categorical,
            "first_timestamp": self._first_timestamp,
            "last_timestamp": self._last_timestamp,
        }
