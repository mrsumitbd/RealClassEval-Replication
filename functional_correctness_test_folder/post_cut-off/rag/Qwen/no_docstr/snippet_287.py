
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class InputInterval:
    '''Input interval values to query.'''
    time_window: Optional[str] = field(default=None)
    relative_time: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InputInterval':
        '''Create from a dictionary.'''
        return cls(**data)

    def __post_init__(self):
        '''Validate that only one of `time_window` or `relative_time` is set.'''
        if self.time_window is not None and self.relative_time is not None:
            raise ValueError(
                "Only one of 'time_window' or 'relative_time' can be set.")
        if self.time_window is None and self.relative_time is None:
            raise ValueError(
                "Either 'time_window' or 'relative_time' must be set.")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to a dictionary.'''
        return {
            'time_window': self.time_window,
            'relative_time': self.relative_time
        }
