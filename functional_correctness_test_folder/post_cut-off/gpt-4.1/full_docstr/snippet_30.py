
from dataclasses import dataclass, field
from typing import Dict, Any
from collections import defaultdict


@dataclass
class UsageEntry:
    '''Dummy UsageEntry for demonstration.'''
    user: str
    usage: float
    count: int

    def to_dict(self):
        return {'user': self.user, 'usage': self.usage, 'count': self.count}


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage: float = 0.0
    total_count: int = 0
    user_stats: Dict[str, Dict[str, float]] = field(
        default_factory=lambda: defaultdict(lambda: {'usage': 0.0, 'count': 0}))

    def add_entry(self, entry: UsageEntry) -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.total_usage += entry.usage
        self.total_count += entry.count
        stats = self.user_stats[entry.user]
        stats['usage'] += entry.usage
        stats['count'] += entry.count

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_usage': self.total_usage,
            'total_count': self.total_count,
            'user_stats': {user: dict(stats) for user, stats in self.user_stats.items()}
        }
