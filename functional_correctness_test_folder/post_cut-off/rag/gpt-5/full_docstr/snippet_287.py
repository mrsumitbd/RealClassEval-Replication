from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple, Union
import re


def _parse_datetime(value: Union[str, datetime]) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError as e:
            raise ValueError(f"Invalid datetime string: {value}") from e
    raise ValueError(f"Unsupported datetime value type: {type(value)}")


def _parse_time_window(value: Any) -> Tuple[datetime, datetime]:
    if isinstance(value, dict):
        if "start" not in value or "end" not in value:
            raise ValueError(
                "time_window dict must contain 'start' and 'end' keys")
        start = _parse_datetime(value["start"])
        end = _parse_datetime(value["end"])
        return start, end
    if isinstance(value, (list, tuple)) and len(value) == 2:
        start = _parse_datetime(value[0])
        end = _parse_datetime(value[1])
        return start, end
    raise ValueError(
        "time_window must be a dict with 'start'/'end' or a 2-item list/tuple")


_TIMEUNIT_TO_SECONDS = {
    "d": 86400.0,
    "h": 3600.0,
    "m": 60.0,
    "s": 1.0,
}


def _parse_relative_time(value: Any) -> timedelta:
    if isinstance(value, timedelta):
        return value
    if isinstance(value, (int, float)):
        return timedelta(seconds=float(value))
    if isinstance(value, str):
        s = value.strip().lower()
        # Allow simple compound duration like "1h30m", "2d", "45s", with optional spaces.
        parts = re.findall(r"(\d+(?:\.\d*)?)\s*([dhms])", s)
        if parts:
            total_seconds = 0.0
            for num_str, unit in parts:
                total_seconds += float(num_str) * _TIMEUNIT_TO_SECONDS[unit]
            return timedelta(seconds=total_seconds)
        # Fallback: try plain number in string (seconds)
        try:
            return timedelta(seconds=float(s))
        except ValueError:
            pass
    raise ValueError(
        "relative_time must be timedelta, number of seconds, or a duration string like '1h30m'")


@dataclass
class InputInterval:
    """Input interval values to query."""
    time_window: Optional[Tuple[datetime, datetime]] = None
    relative_time: Optional[timedelta] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")
        tw = rt = None
        if "time_window" in data and data["time_window"] is not None:
            tw = _parse_time_window(data["time_window"])
        if "relative_time" in data and data["relative_time"] is not None:
            rt = _parse_relative_time(data["relative_time"])
        return cls(time_window=tw, relative_time=rt)

    def __post_init__(self):
        """Validate that only one of `time_window` or `relative_time` is set."""
        has_tw = self.time_window is not None
        has_rt = self.relative_time is not None
        if has_tw == has_rt:
            raise ValueError(
                "Exactly one of 'time_window' or 'relative_time' must be set")

        if self.time_window is not None:
            start, end = self.time_window
            if not isinstance(start, datetime) or not isinstance(end, datetime):
                raise ValueError(
                    "time_window must be a tuple of two datetime objects")
            if end <= start:
                raise ValueError("time_window end must be after start")

        if self.relative_time is not None:
            if not isinstance(self.relative_time, timedelta):
                raise ValueError("relative_time must be a timedelta")
            if self.relative_time.total_seconds() <= 0:
                raise ValueError("relative_time must be positive")

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
        # relative_time
        seconds = self.relative_time.total_seconds()
        value = int(seconds) if float(seconds).is_integer() else seconds
        return {"relative_time": value}
