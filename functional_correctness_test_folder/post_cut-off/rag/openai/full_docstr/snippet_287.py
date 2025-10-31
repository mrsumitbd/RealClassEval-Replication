
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple, Union


def _parse_timedelta(value: Union[int, float, str]) -> timedelta:
    """Parse a relative time value into a timedelta."""
    if isinstance(value, (int, float)):
        return timedelta(seconds=float(value))
    if isinstance(value, str):
        value = value.strip().lower()
        if value.endswith("d"):
            return timedelta(days=float(value[:-1]))
        if value.endswith("h"):
            return timedelta(hours=float(value[:-1]))
        if value.endswith("m"):
            return timedelta(minutes=float(value[:-1]))
        if value.endswith("s"):
            return timedelta(seconds=float(value[:-1]))
        # fallback: assume seconds
        try:
            return timedelta(seconds=float(value))
        except ValueError as exc:
            raise ValueError(
                f"Cannot parse relative time string: {value}") from exc
    raise TypeError(f"Unsupported type for relative time: {type(value)}")


@dataclass
class InputInterval:
    """Input interval values to query."""

    time_window: Optional[Tuple[datetime, datetime]] = field(default=None)
    relative_time: Optional[timedelta] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InputInterval":
        """Create from a dictionary."""
        if "time_window" in data and "relative_time" in data:
            raise ValueError(
                "Both 'time_window' and 'relative_time' provided; only one allowed.")
        if "time_window" in data:
            tw = data["time_window"]
            if not isinstance(tw, dict):
                raise TypeError(
                    "'time_window' must be a dict with 'start' and 'end' keys.")
            try:
                start = datetime.fromisoformat(tw["start"])
                end = datetime.fromisoformat(tw["end"])
            except Exception as exc:
                raise ValueError(
                    "Invalid datetime format in 'time_window'") from exc
            return cls(time_window=(start, end))
        if "relative_time" in data:
            rel = _parse_timedelta(data["relative_time"])
            return cls(relative_time=rel)
        raise ValueError(
            "Either 'time_window' or 'relative_time' must be provided.")

    def __post_init__(self) -> None:
        """Validate that only one of `time_window` or `relative_time` is set."""
        if (self.time_window is None) == (self.relative_time is None):
            raise ValueError(
                "Exactly one of 'time_window' or 'relative_time' must be set."
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
        if self.relative_time is not None:
            # Represent relative time in seconds
            return {"relative_time": int(self.relative_time.total_seconds())}
        # Should never reach here due to __post_init__
        raise RuntimeError("InputInterval is in an invalid state.")
