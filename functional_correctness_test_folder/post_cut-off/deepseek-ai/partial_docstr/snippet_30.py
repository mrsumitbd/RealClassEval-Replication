
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage: float = 0.0
    count: int = 0
    min_usage: float = float('inf')
    max_usage: float = float('-inf')

    def add_entry(self, entry: UsageEntry) -> None:
        self.total_usage += entry.usage
        self.count += 1
        if entry.usage < self.min_usage:
            self.min_usage = entry.usage
        if entry.usage > self.max_usage:
            self.max_usage = entry.usage

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_usage': self.total_usage,
            'count': self.count,
            'min_usage': self.min_usage if self.count > 0 else None,
            'max_usage': self.max_usage if self.count > 0 else None,
            'avg_usage': self.total_usage / self.count if self.count > 0 else None
        }
