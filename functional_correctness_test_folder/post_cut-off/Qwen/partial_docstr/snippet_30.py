
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class UsageEntry:
    user_id: int
    usage_time: float


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage: float = 0.0
    entries: List[UsageEntry] = field(default_factory=list)

    def add_entry(self, entry: UsageEntry) -> None:
        self.entries.append(entry)
        self.total_usage += entry.usage_time

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_usage': self.total_usage,
            'entries': [{'user_id': entry.user_id, 'usage_time': entry.usage_time} for entry in self.entries]
        }
