
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Union


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    _entries: List[Any] = field(default_factory=list, init=False, repr=False)

    def add_entry(self, entry: Any) -> None:
        """Add an entry's statistics to this aggregate."""
        self._entries.append(entry)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        if not self._entries:
            return {"entries": [], "total_entries": 0}

        # Basic metadata
        result: Dict[str, Any] = {
            "total_entries": len(self._entries),
            "entries": [],
        }

        # If entries are dataclasses or objects with __dict__, use that
        first = self._entries[0]
        if hasattr(first, "__dict__"):
            keys = list(first.__dict__.keys())
        else:
            # Assume entry is a mapping or tuple/list
            if isinstance(first, dict):
                keys = list(first.keys())
            else:
                # Fallback: treat entry as a single value
                keys = ["value"]

        # Aggregate numeric fields
        numeric_stats: Dict[str, Dict[str, Union[int, float]]] = {}
        for key in keys:
            values = []
            for e in self._entries:
                val = None
                if hasattr(e, "__dict__"):
                    val = e.__dict__.get(key)
                elif isinstance(e, dict):
                    val = e.get(key)
                else:
                    # If entry is a single value and key is "value"
                    if key == "value":
                        val = e
                if isinstance(val, (int, float)):
                    values.append(val)
            if values:
                numeric_stats[key] = {
                    "count": len(values),
                    "sum": sum(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                }

        result["numeric_stats"] = numeric_stats

        # Store raw entries for reference
        for e in self._entries:
            if hasattr(e, "__dict__"):
                result["entries"].append(e.__dict__)
            elif isinstance(e, dict):
                result["entries"].append(e)
            else:
                result["entries"].append({"value": e})

        return result
