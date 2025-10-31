
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Union

# The actual UsageEntry type is not defined in this snippet.
# It is expected to be a dataclass or similar object with numeric attributes.
# For type‑checking purposes we can use a forward reference.
try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from typing import Protocol

        class UsageEntryProtocol(Protocol):
            """Protocol for a usage entry with numeric attributes."""

            def __iter__(self) -> Any: ...
except Exception:
    pass


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""

    # Store the raw entries for potential future use
    _entries: List[Any] = field(default_factory=list, init=False, repr=False)

    # Aggregated numeric statistics
    _sums: Dict[str, float] = field(
        default_factory=dict, init=False, repr=False)
    _mins: Dict[str, float] = field(
        default_factory=dict, init=False, repr=False)
    _maxs: Dict[str, float] = field(
        default_factory=dict, init=False, repr=False)

    def add_entry(self, entry: Any) -> None:
        """Add an entry's statistics to this aggregate."""
        self._entries.append(entry)

        # Iterate over the entry's attributes.  We accept any object that
        # provides a __dict__ or is iterable of (key, value) pairs.
        if hasattr(entry, "__dict__"):
            items = entry.__dict__.items()
        else:
            try:
                items = entry
            except TypeError:
                # If entry is not iterable, skip it
                return

        for key, value in items:
            if isinstance(value, (int, float)):
                # Update sum
                self._sums[key] = self._sums.get(key, 0.0) + float(value)

                # Update min
                if key not in self._mins or value < self._mins[key]:
                    self._mins[key] = float(value)

                # Update max
                if key not in self._maxs or value > self._maxs[key]:
                    self._maxs[key] = float(value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result: Dict[str, Any] = {
            "num_entries": len(self._entries),
        }

        for key in self._sums:
            sum_val = self._sums[key]
            min_val = self._mins.get(key)
            max_val = self._maxs.get(key)
            avg_val = sum_val / len(self._entries) if self._entries else None

            result[key] = {
                "sum": sum_val,
                "min": min_val,
                "max": max_val,
                "avg": avg_val,
            }

        return result
