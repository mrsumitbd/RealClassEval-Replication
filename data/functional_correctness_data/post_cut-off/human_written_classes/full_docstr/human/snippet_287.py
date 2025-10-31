from typing import Any, Dict, List, Optional, Union
from dataclasses import asdict, dataclass, field

@dataclass
class InputInterval:
    """Input interval values to query."""
    time_window: Optional[Dict[str, Any]] = None
    relative_time: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from a dictionary."""
        return cls(time_window=data.get('time_window') or data.get('timeWindow'), relative_time=data.get('relative_time') or data.get('relativeTime'))

    def __post_init__(self):
        """Validate that only one of `time_window` or `relative_time` is set."""
        if self.time_window is not None and self.relative_time is not None:
            raise ValueError('Only one of `time_window` or `relative_time` can be set.')
        if self.time_window is None and self.relative_time is None:
            raise ValueError('One of `time_window` or `relative_time` must be set.')

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        result = {}
        if self.time_window:
            result['timeWindow'] = self.time_window
        if self.relative_time:
            result['relativeTime'] = self.relative_time
        return result