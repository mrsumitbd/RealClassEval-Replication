from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    total_count: int = 0
    total_duration: float = 0.0
    min_duration: float = field(default_factory=lambda: float('inf'))
    max_duration: float = field(default_factory=lambda: float('-inf'))

    def add_entry(self, entry: 'UsageEntry') -> None:
        """Add an entry's statistics to this aggregate."""
        self.total_count += 1
        self.total_duration += entry.duration
        if entry.duration < self.min_duration:
            self.min_duration = entry.duration
        if entry.duration > self.max_duration:
            self.max_duration = entry.duration

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "total_count": self.total_count,
            "total_duration": self.total_duration,
            "min_duration": None if self.total_count == 0 else self.min_duration,
            "max_duration": None if self.total_count == 0 else self.max_duration,
        }
