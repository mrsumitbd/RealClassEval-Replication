
from dataclasses import dataclass, field
from typing import Dict, Any, List
from collections import defaultdict


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage: float = 0.0
    entry_count: int = 0
    usage_by_category: Dict[str, float] = field(
        default_factory=lambda: defaultdict(float))
    usage_by_user: Dict[str, float] = field(
        default_factory=lambda: defaultdict(float))

    def add_entry(self, entry: UsageEntry) -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.total_usage += entry.usage
        self.entry_count += 1
        self.usage_by_category[entry.category] += entry.usage
        self.usage_by_user[entry.user_id] += entry.usage

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_usage': self.total_usage,
            'entry_count': self.entry_count,
            'usage_by_category': dict(self.usage_by_category),
            'usage_by_user': dict(self.usage_by_user)
        }
