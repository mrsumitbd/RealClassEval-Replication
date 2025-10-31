
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage: float = 0.0
    count: int = 0

    def add_entry(self, entry: 'UsageEntry') -> None:
        self.total_usage += entry.usage
        self.count += 1

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_usage': self.total_usage,
            'count': self.count
        }
