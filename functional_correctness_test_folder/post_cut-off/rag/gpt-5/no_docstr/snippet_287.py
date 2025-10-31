from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class InputInterval:
    """Input interval values to query."""
    time_window: Optional[Dict[str, Any]] = None
    relative_time: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from a dictionary."""
        if data is None or not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if "time_window" in data or "relative_time" in data:
            return cls(
                time_window=data.get("time_window"),
                relative_time=data.get("relative_time"),
            )

        start = data.get("start") or data.get("start_time")
        end = data.get("end") or data.get("end_time")
        if start is not None or end is not None:
            tw: Dict[str, Any] = {}
            if start is not None:
                tw["start"] = start
            if end is not None:
                tw["end"] = end
            return cls(time_window=tw)

        duration = data.get("duration") or data.get("relative")
        if duration is not None:
            return cls(relative_time=duration)

        # Fallback to trigger validation error (none set)
        return cls()

    def __post_init__(self):
        """Validate that only one of `time_window` or `relative_time` is set."""
        if self.time_window is not None and not isinstance(self.time_window, dict):
            raise TypeError("time_window must be a dictionary when provided")

        has_tw = self.time_window is not None
        has_rt = self.relative_time is not None
        if has_tw == has_rt:
            raise ValueError(
                "Exactly one of 'time_window' or 'relative_time' must be set.")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        if self.time_window is not None:
            return {"time_window": self.time_window}
        return {"relative_time": self.relative_time}
