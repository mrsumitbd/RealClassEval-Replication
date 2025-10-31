
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_entries: int = 0
    total_duration: float = 0.0
    total_volume: float = 0.0
    total_moves: int = 0
    total_temperature: float = 0.0
    total_pressure: float = 0.0

    def add_entry(self, entry: UsageEntry) -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.total_entries += 1
        self.total_duration += entry.duration
        self.total_volume += entry.volume
        self.total_moves += entry.moves
        self.total_temperature += entry.temperature
        self.total_pressure += entry.pressure

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        return {
            'total_entries': self.total_entries,
            'total_duration': self.total_duration,
            'total_volume': self.total_volume,
            'total_moves': self.total_moves,
            'total_temperature': self.total_temperature,
            'total_pressure': self.total_pressure
        }
