
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple


@dataclass
class InputInterval:
    """Input interval values to query."""

    time_window: Optional[Tuple[datetime, datetime]] = field(default=None)
    relative_time: Optional[timedelta] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InputInterval":
        """Create from a dictionary."""
        time_window = None
        relative_time = None

        if "time_window" in data:
            tw = data["time_window"]
            if not isinstance(tw, (list, tuple)) or len(tw) != 2:
                raise ValueError(
                    "time_window must be a list/tuple of two datetime strings")
            try:
                start = datetime.fromisoformat(tw[0])
                end = datetime.fromisoformat(tw[1])
            except Exception as exc:
                raise ValueError(
                    f"Invalid datetime format in time_window: {exc}") from exc
            time_window = (start, end)

        if "relative_time" in data:
            rt = data["relative_time"]
            if isinstance(rt, (int, float)):
                relative_time = timedelta(seconds=rt)
            elif isinstance(rt, str):
                try:
                    # allow ISO 8601 duration like "PT5M" or simple seconds string
                    if rt.upper().startswith("PT"):
                        # naive parsing: only seconds
                        if rt.upper().endswith("S"):
                            seconds = int(rt[2:-1])
                            relative_time = timedelta(seconds=seconds)
                        else:
                            raise ValueError
                    else:
                        relative_time = timedelta(seconds=float(rt))
                except Exception as exc:
                    raise ValueError(
                        f"Invalid relative_time format: {exc}") from exc
            else:
                raise ValueError("relative_time must be a number or string")

        return cls(time_window=time_window, relative_time=relative_time)

    def __post_init__(self) -> None:
        """Validate that only one of `time_window` or `relative_time` is set."""
        if self.time_window is not None and self.relative_time is not None:
            raise ValueError(
                "Only one of time_window or relative_time may be set")
        if self.time_window is None and self.relative_time is None:
            raise ValueError("Either time_window or relative_time must be set")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        if self.time_window is not None:
            return {
                "time_window": [
                    self.time_window[0].isoformat(),
                    self.time_window[1].isoformat(),
                ]
            }
        if self.relative_time is not None:
            # store as seconds
            return {"relative_time": int(self.relative_time.total_seconds())}
        return {}
