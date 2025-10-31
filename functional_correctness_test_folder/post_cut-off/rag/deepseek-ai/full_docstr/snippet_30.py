
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    total_usage: int = 0
    count: int = 0
    max_usage: int = 0
    min_usage: int = 0

    def add_entry(self, entry: UsageEntry) -> None:
        """Add an entry's statistics to this aggregate."""
        self.total_usage += entry.usage
        self.count += 1
        if entry.usage > self.max_usage:
            self.max_usage = entry.usage
        if self.count == 1 or entry.usage < self.min_usage:
            self.min_usage = entry.usage

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "total_usage": self.total_usage,
            "count": self.count,
            "max_usage": self.max_usage,
            "min_usage": self.min_usage,
            "average_usage": self.total_usage / self.count if self.count > 0 else 0
        }
