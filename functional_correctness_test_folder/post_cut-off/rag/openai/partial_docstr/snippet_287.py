
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union


def _parse_datetime(value: Union[str, datetime]) -> datetime:
    """Parse a datetime from a string or return it unchanged."""
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


@dataclass
class InputInterval:
    """Input interval values to query."""

    time_window: Optional[Tuple[datetime, datetime]] = None
    relative_time: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InputInterval":
        """Create from a dictionary."""
        time_window = None
        relative_time = None

        if "time_window" in data:
            tw = data["time_window"]
            if isinstance(tw, dict):
                start = _parse_datetime(tw.get("start"))
                end = _parse_datetime(tw.get("end"))
            elif isinstance(tw, (list, tuple)) and len(tw) == 2:
                start = _parse_datetime(tw[0])
                end = _parse_datetime(tw[1])
            else:
                raise ValueError(
                    "time_window must be a dict with 'start'/'end' or a list of two ISO strings")
            time_window = (start, end)

        if "relative_time" in data:
            relative_time = str(data["relative_time"])

        return cls(time_window=time_window, relative_time=relative_time)

    def __post_init__(self) -> None:
        """Validate that only one of `time_window` or `relative_time` is set."""
        if (self.time_window is None) == (self.relative_time is None):
            raise ValueError(
                "Exactly one of `time_window` or `relative_time` must be set"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        if self.time_window is not None:
            start, end = self.time_window
            return {
                "time_window": {
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                }
            }
        else:
            return {"relative_time": self.relative_time}
