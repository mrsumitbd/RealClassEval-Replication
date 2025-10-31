
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union


@dataclass
class InputInterval:
    """Input interval values to query."""

    # One of these must be set, but not both.
    time_window: Optional[Tuple[datetime, datetime]] = None
    relative_time: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InputInterval":
        """Create from a dictionary."""
        time_window = None
        relative_time = None

        if "time_window" in data:
            tw = data["time_window"]
            # Accept either a dict with 'start'/'end' or a list/tuple of two ISO strings
            if isinstance(tw, dict):
                start = tw.get("start")
                end = tw.get("end")
            elif isinstance(tw, (list, tuple)) and len(tw) == 2:
                start, end = tw
            else:
                raise ValueError(
                    "time_window must be a dict with 'start'/'end' or a list/tuple of two items")

            if start is None or end is None:
                raise ValueError(
                    "time_window must contain both 'start' and 'end' values")

            # Parse ISO strings to datetime if necessary
            if isinstance(start, str):
                start = datetime.fromisoformat(start)
            if isinstance(end, str):
                end = datetime.fromisoformat(end)

            if not isinstance(start, datetime) or not isinstance(end, datetime):
                raise TypeError(
                    "time_window start and end must be datetime objects or ISO strings")

            time_window = (start, end)

        if "relative_time" in data:
            relative_time = data["relative_time"]

        return cls(time_window=time_window, relative_time=relative_time)

    def __post_init__(self) -> None:
        """Validate that only one of `time_window` or `relative_time` is set."""
        if (self.time_window is None) == (self.relative_time is None):
            raise ValueError(
                "Exactly one of `time_window` or `relative_time` must be set"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        result: Dict[str, Any] = {}
        if self.time_window is not None:
            start, end = self.time_window
            result["time_window"] = {
                "start": start.isoformat() if isinstance(start, datetime) else start,
                "end": end.isoformat() if isinstance(end, datetime) else end,
            }
        if self.relative_time is not None:
            result["relative_time"] = self.relative_time
        return result
