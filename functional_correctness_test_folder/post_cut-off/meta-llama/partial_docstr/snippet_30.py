
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage: int = field(default=0, init=False)
    num_entries: int = field(default=0, init=False)
    max_usage: int = field(default=0, init=False)
    min_usage: int = field(default=float('inf'), init=False)

    def add_entry(self, entry: 'UsageEntry') -> None:
        self.total_usage += entry.usage
        self.num_entries += 1
        self.max_usage = max(self.max_usage, entry.usage)
        self.min_usage = min(self.min_usage, entry.usage)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_usage': self.total_usage,
            'average_usage': self.total_usage / self.num_entries if self.num_entries > 0 else 0,
            'num_entries': self.num_entries,
            'max_usage': self.max_usage,
            'min_usage': self.min_usage if self.min_usage != float('inf') else None
        }
