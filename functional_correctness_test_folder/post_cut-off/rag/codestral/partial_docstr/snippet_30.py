
from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_entries: int = 0
    total_duration: float = 0.0
    start_time: datetime = None
    end_time: datetime = None
    entry_types: Dict[str, int] = None

    def __post_init__(self):
        if self.entry_types is None:
            self.entry_types = {}

    def add_entry(self, entry: UsageEntry) -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.total_entries += 1
        self.total_duration += entry.duration
        if self.start_time is None or entry.start_time < self.start_time:
            self.start_time = entry.start_time
        if self.end_time is None or entry.end_time > self.end_time:
            self.end_time = entry.end_time
        entry_type = entry.entry_type
        if entry_type in self.entry_types:
            self.entry_types[entry_type] += 1
        else:
            self.entry_types[entry_type] = 1

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_entries': self.total_entries,
            'total_duration': self.total_duration,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'entry_types': self.entry_types
        }
