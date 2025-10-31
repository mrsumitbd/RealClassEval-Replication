
from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class AggregatedStats:
    total_usage: float = 0.0
    count: int = 0
    min_usage: float = float('inf')
    max_usage: float = float('-inf')

    def add_entry(self, entry: 'UsageEntry') -> None:
        usage = entry.usage
        self.total_usage += usage
        self.count += 1
        if usage < self.min_usage:
            self.min_usage = usage
        if usage > self.max_usage:
            self.max_usage = usage

    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_usage': self.total_usage,
            'count': self.count,
            'min_usage': self.min_usage if self.count > 0 else 0.0,
            'max_usage': self.max_usage if self.count > 0 else 0.0,
            'avg_usage': self.total_usage / self.count if self.count > 0 else 0.0
        }
