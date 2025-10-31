
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_count: int = field(default=0, init=False)
    total_duration: float = field(default=0.0, init=False)
    total_size: int = field(default=0, init=False)

    def add_entry(self, entry: 'UsageEntry') -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.total_count += entry.count
        self.total_duration += entry.duration
        self.total_size += entry.size

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_count': self.total_count,
            'total_duration': self.total_duration,
            'total_size': self.total_size,
            'average_duration': self.total_duration / self.total_count if self.total_count > 0 else 0.0,
            'average_size': self.total_size / self.total_count if self.total_count > 0 else 0,
        }
