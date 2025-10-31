
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Union

Number = Union[int, float]


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""

    total_entries: int = 0
    _sums: Dict[str, Number] = field(default_factory=dict)

    def add_entry(self, entry: Any) -> None:
        """Add an entry's statistics to this aggregate."""
        # Accept any object that has a __dict__ or is a mapping
        if hasattr(entry, "__dict__"):
            data: Iterable[tuple[str, Any]] = entry.__dict__.items()
        elif isinstance(entry, dict):
            data = entry.items()
        else:
            # Try to iterate over attributes
            data = ((k, getattr(entry, k)) for k in dir(entry)
                    if not k.startswith("_") and not callable(getattr(entry, k)))

        for key, value in data:
            if isinstance(value, (int, float)):
                self._sums[key] = self._sums.get(key, 0) + value

        self.total_entries += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result: Dict[str, Any] = {"total_entries": self.total_entries}
        for key, total in self._sums.items():
            result[f"{key}_sum"] = total
            if self.total_entries:
                result[f"{key}_avg"] = total / self.total_entries
        return result
