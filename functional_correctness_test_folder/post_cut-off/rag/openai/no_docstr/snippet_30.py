
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Union

Number = Union[int, float]


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""

    # Store all entries that have been added
    entries: List[Any] = field(default_factory=list)

    # Aggregated numeric statistics
    total_count: int = 0
    total_sum: float = 0.0
    min_value: Number | None = None
    max_value: Number | None = None

    def _extract_value(self, entry: Any) -> Number | None:
        """
        Try to extract a numeric value from an entry.

        The function looks for a `value` attribute, a `usage` attribute,
        or treats the entry itself as a number if it is an int/float.
        """
        if isinstance(entry, (int, float)):
            return entry
        for attr in ("value", "usage"):
            if hasattr(entry, attr):
                val = getattr(entry, attr)
                if isinstance(val, (int, float)):
                    return val
        return None

    def add_entry(self, entry: Any) -> None:
        """Add an entry's statistics to this aggregate."""
        self.entries.append(entry)

        val = self._extract_value(entry)
        if val is None:
            return  # nothing to aggregate

        self.total_count += 1
        self.total_sum += float(val)

        if self.min_value is None or val < self.min_value:
            self.min_value = val
        if self.max_value is None or val > self.max_value:
            self.max_value = val

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        avg = (
            self.total_sum / self.total_count if self.total_count > 0 else None
        )
        # Convert entries to dicts if possible, otherwise keep as is
        entries_repr = []
        for e in self.entries:
            if hasattr(e, "to_dict") and callable(e.to_dict):
                entries_repr.append(e.to_dict())
            else:
                entries_repr.append(e)

        return {
            "count": self.total_count,
            "sum": self.total_sum,
            "min": self.min_value,
            "max": self.max_value,
            "average": avg,
            "entries": entries_repr,
        }
