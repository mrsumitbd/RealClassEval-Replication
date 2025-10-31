from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Dict, Any, Mapping
from collections import Counter


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    _numeric_sums: Dict[str, float] = field(default_factory=dict)
    _numeric_mins: Dict[str, float] = field(default_factory=dict)
    _numeric_maxs: Dict[str, float] = field(default_factory=dict)
    _numeric_counts: Dict[str, int] = field(default_factory=dict)
    _bool_true_counts: Dict[str, int] = field(default_factory=dict)
    _bool_false_counts: Dict[str, int] = field(default_factory=dict)
    _categorical_counts: Dict[str, Counter] = field(default_factory=dict)
    _entries_count: int = 0

    def _entry_to_mapping(self, entry: Any) -> Dict[str, Any]:
        if entry is None:
            return {}
        if isinstance(entry, Mapping):
            return dict(entry)
        if hasattr(entry, "to_dict") and callable(getattr(entry, "to_dict")):
            try:
                d = entry.to_dict()
                if isinstance(d, Mapping):
                    return dict(d)
            except Exception:
                pass
        if is_dataclass(entry):
            try:
                return asdict(entry)
            except Exception:
                pass
        try:
            return dict(vars(entry))
        except Exception:
            return {}

    def add_entry(self, entry: 'UsageEntry') -> None:
        """Add an entry's statistics to this aggregate."""
        data = self._entry_to_mapping(entry)
        if not data:
            self._entries_count += 1
            return

        for key, value in data.items():
            # Booleans: track true/false counts
            if isinstance(value, bool):
                if value:
                    self._bool_true_counts[key] = self._bool_true_counts.get(
                        key, 0) + 1
                else:
                    self._bool_false_counts[key] = self._bool_false_counts.get(
                        key, 0) + 1
                continue

            # Numeric (int/float) excluding booleans
            if isinstance(value, (int, float)):
                self._numeric_sums[key] = self._numeric_sums.get(
                    key, 0.0) + float(value)
                self._numeric_counts[key] = self._numeric_counts.get(
                    key, 0) + 1
                if key not in self._numeric_mins or float(value) < self._numeric_mins[key]:
                    self._numeric_mins[key] = float(value)
                if key not in self._numeric_maxs or float(value) > self._numeric_maxs[key]:
                    self._numeric_maxs[key] = float(value)
                continue

            # Categorical strings: keep frequency counts
            if isinstance(value, str):
                self._categorical_counts.setdefault(key, Counter())
                self._categorical_counts[key][value] += 1
                continue

            # Ignore other types silently

        self._entries_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        means = {k: (self._numeric_sums[k] / self._numeric_counts[k])
                 for k in self._numeric_sums.keys() if self._numeric_counts.get(k, 0) > 0}
        categorical = {k: dict(v) for k, v in self._categorical_counts.items()}
        return {
            "count": self._entries_count,
            "numeric": {
                "sum": dict(self._numeric_sums),
                "min": dict(self._numeric_mins),
                "max": dict(self._numeric_maxs),
                "mean": means,
                "count": dict(self._numeric_counts),
            },
            "booleans": {
                "true": dict(self._bool_true_counts),
                "false": dict(self._bool_false_counts),
            },
            "categorical": categorical,
        }
