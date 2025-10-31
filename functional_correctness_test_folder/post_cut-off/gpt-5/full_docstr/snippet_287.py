from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class InputInterval:
    '''Input interval values to query.'''
    time_window: Optional[Dict[str, Any]] = None
    relative_time: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        '''Create from a dictionary.'''
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        time_window = data.get("time_window")
        relative_time = data.get("relative_time")
        return cls(time_window=time_window, relative_time=relative_time)

    def __post_init__(self):
        '''Validate that only one of `time_window` or `relative_time` is set.'''
        if (self.time_window is None) == (self.relative_time is None):
            raise ValueError(
                "Exactly one of `time_window` or `relative_time` must be set.")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to a dictionary.'''
        if self.time_window is not None:
            return {"time_window": self.time_window}
        return {"relative_time": self.relative_time}
