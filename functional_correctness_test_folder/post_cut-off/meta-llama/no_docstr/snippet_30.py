
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AggregatedStats:
    total_usage: int = field(default=0, init=False)
    total_duration: int = field(default=0, init=False)
    max_usage: int = field(default=0, init=False)
    min_usage: int = field(default=float('inf'), init=False)
    count: int = field(default=0, init=False)

    def add_entry(self, entry: 'UsageEntry') -> None:
        self.total_usage += entry.usage
        self.total_duration += entry.duration
        self.max_usage = max(self.max_usage, entry.usage)
        self.min_usage = min(self.min_usage, entry.usage)
        self.count += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_usage': self.total_usage,
            'total_duration': self.total_duration,
            'max_usage': self.max_usage,
            'min_usage': self.min_usage if self.min_usage != float('inf') else 0,
            'average_usage': self.total_usage / self.count if self.count > 0 else 0,
            'count': self.count
        }
