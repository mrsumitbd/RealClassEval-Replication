
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class UsageEntry:
    '''A single usage entry.'''
    user_id: int
    usage_time: float
    data_used: float


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage_time: float = 0.0
    total_data_used: float = 0.0
    user_count: int = 0
    users: Dict[int, Dict[str, float]] = field(default_factory=dict)

    def add_entry(self, entry: UsageEntry) -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.total_usage_time += entry.usage_time
        self.total_data_used += entry.data_used
        if entry.user_id not in self.users:
            self.users[entry.user_id] = {'usage_time': 0.0, 'data_used': 0.0}
            self.user_count += 1
        self.users[entry.user_id]['usage_time'] += entry.usage_time
        self.users[entry.user_id]['data_used'] += entry.data_used

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_usage_time': self.total_usage_time,
            'total_data_used': self.total_data_used,
            'user_count': self.user_count,
            'users': self.users
        }
