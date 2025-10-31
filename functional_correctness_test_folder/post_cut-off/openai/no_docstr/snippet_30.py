
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Assume a minimal interface for UsageEntry
# The aggregator will look for a numeric `value` attribute on each entry.
# If an entry does not have this attribute, it will be ignored in the statistics.


class UsageEntry:
    """Placeholder for the real UsageEntry implementation."""
    value: float  # The numeric value to aggregate


@dataclass
class AggregatedStats:
    """Collects and aggregates numeric values from UsageEntry objects."""
    entries: List[UsageEntry] = field(default_factory=list)

    def add_entry(self, entry: UsageEntry) -> None:
        """Add a new entry to the aggregation."""
        self.entries.append(entry)

    def to_dict(self) -> Dict[str, Any]:
        """Return aggregated statistics as a dictionary."""
        # Extract numeric values from entries that expose a `value` attribute.
        values: List[float] = [
            getattr(e, "value") for e in self.entries if hasattr(e, "value")
        ]

        if not values:
            return {
                "count": 0,
                "sum": 0,
                "min": None,
                "max": None,
                "average": None,
            }

        total = sum(values)
        count = len(values)
        return {
            "count": count,
            "sum": total,
            "min": min(values),
            "max": max(values),
            "average": total / count,
        }
