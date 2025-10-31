
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class UsageEntry:
    '''A single usage entry.'''
    duration: float
    usage_count: int


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_duration: float = 0.0
    total_count: int = 0
    entries: List[UsageEntry] = field(default_factory=list)

    def add_entry(self, entry: UsageEntry) -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.total_duration += entry.duration
        self.total_count += entry.usage_count
        self.entries.append(entry)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_duration': self.total_duration,
            'total_count': self.total_count,
            'entries': [{'duration': entry.duration, 'usage_count': entry.usage_count} for entry in self.entries]
        }
