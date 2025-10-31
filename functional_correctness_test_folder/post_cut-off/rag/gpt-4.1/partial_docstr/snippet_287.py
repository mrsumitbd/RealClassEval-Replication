from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple


@dataclass
class InputInterval:
    """Input interval values to query."""
    time_window: Optional[Tuple[str, str]] = field(default=None)
    relative_time: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from a dictionary."""
        time_window = data.get("time_window")
        relative_time = data.get("relative_time")
        return cls(time_window=time_window, relative_time=relative_time)

    def __post_init__(self):
        """Validate that only one of `time_window` or `relative_time` is set."""
        if self.time_window is not None and self.relative_time is not None:
            raise ValueError(
                "Only one of 'time_window' or 'relative_time' may be set.")
        if self.time_window is None and self.relative_time is None:
            raise ValueError(
                "One of 'time_window' or 'relative_time' must be set.")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        result = {}
        if self.time_window is not None:
            result["time_window"] = self.time_window
        if self.relative_time is not None:
            result["relative_time"] = self.relative_time
        return result
