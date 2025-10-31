from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple, Union
import re


def _parse_datetime(value: Union[str, int, float, datetime]) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        s = value.strip()
        # Handle Zulu time
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(s)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            # Try numeric epoch string
            try:
                return datetime.fromtimestamp(float(s), tz=timezone.utc)
            except Exception:
                pass
    raise ValueError(f"Unsupported datetime format: {value!r}")


_UNIT_TO_KWARG = {
    "s": "seconds",
    "sec": "seconds",
    "secs": "seconds",
    "second": "seconds",
    "seconds": "seconds",
    "m": "minutes",
    "min": "minutes",
    "mins": "minutes",
    "minute": "minutes",
    "minutes": "minutes",
    "h": "hours",
    "hr": "hours",
    "hrs": "hours",
    "hour": "hours",
    "hours": "hours",
    "d": "days",
    "day": "days",
    "days": "days",
    "w": "weeks",
    "wk": "weeks",
    "wks": "weeks",
    "week": "weeks",
    "weeks": "weeks",
}


def _parse_relative(value: Any) -> timedelta:
    if isinstance(value, timedelta):
        return value
    if isinstance(value, (int, float)):
        return timedelta(seconds=float(value))
    if isinstance(value, str):
        s = value.strip().lower()
        # ISO8601-like "PnDTnHnMnS" minimal handling: only days/hours/minutes/seconds
        if s.startswith("p"):
            # Extract numbers before D, T...S
            days = hours = minutes = seconds = 0.0
            # days
            m = re.search(r"(\d+(?:\.\d+)?)d", s)
            if m:
                days = float(m.group(1))
            # time part
            m = re.search(r"t.*?(\d+(?:\.\d+)?)h", s)
            if m:
                hours = float(m.group(1))
            m = re.search(r"t.*?(\d+(?:\.\d+)?)m", s)
            if m:
                minutes = float(m.group(1))
            m = re.search(r"t.*?(\d+(?:\.\d+)?)s", s)
            if m:
                seconds = float(m.group(1))
            total = timedelta(days=days, hours=hours,
                              minutes=minutes, seconds=seconds)
            if total.total_seconds() > 0:
                return total
        # Compact like "1h30m", "45m", "10s", "2d"
        parts = re.findall(r"(\d+(?:\.\d+)?)([smhdw])", s)
        if parts:
            kwargs: Dict[str, float] = {}
            for num, unit in parts:
                key = _UNIT_TO_KWARG[unit]
                kwargs[key] = kwargs.get(key, 0.0) + float(num)
            return timedelta(**kwargs)  # type: ignore[arg-type]
        # Try numeric seconds string
        try:
            return timedelta(seconds=float(s))
        except Exception:
            pass
        raise ValueError(f"Unsupported relative_time string: {value!r}")
    if isinstance(value, dict):
        # Support {'value': 5, 'unit': 'minutes'} or unit-keyed dicts
        if "value" in value and "unit" in value:
            unit = str(value["unit"]).lower().strip()
            if unit not in _UNIT_TO_KWARG:
                raise ValueError(f"Unsupported relative_time unit: {unit!r}")
            key = _UNIT_TO_KWARG[unit]
            # type: ignore[arg-type]
            return timedelta(**{key: float(value["value"])})
        # Unit-keyed dicts e.g. {'seconds': 30, 'minutes': 2}
        kwargs: Dict[str, float] = {}
        for k, v in value.items():
            key = _UNIT_TO_KWARG.get(str(k).lower().strip())
            if key:
                kwargs[key] = kwargs.get(key, 0.0) + float(v)
        if kwargs:
            return timedelta(**kwargs)  # type: ignore[arg-type]
        raise ValueError(f"Unsupported relative_time mapping: {value!r}")
    raise ValueError(f"Unsupported relative_time format: {value!r}")


@dataclass
class InputInterval:
    """Input interval values to query."""
    time_window: Optional[Tuple[datetime, datetime]] = None
    relative_time: Optional[timedelta] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        tw = None
        rt = None

        if "time_window" in data and data["time_window"] is not None:
            tw_val = data["time_window"]
            if isinstance(tw_val, dict):
                if "start" not in tw_val or "end" not in tw_val:
                    raise ValueError(
                        "time_window must contain 'start' and 'end'")
                start = _parse_datetime(tw_val["start"])
                end = _parse_datetime(tw_val["end"])
                tw = (start, end)
            elif isinstance(tw_val, (list, tuple)) and len(tw_val) == 2:
                start = _parse_datetime(tw_val[0])
                end = _parse_datetime(tw_val[1])
                tw = (start, end)
            else:
                raise ValueError(
                    "time_window must be a mapping with 'start'/'end' or a 2-sequence")

        if "relative_time" in data and data["relative_time"] is not None:
            rt = _parse_relative(data["relative_time"])

        return cls(time_window=tw, relative_time=rt)

    def __post_init__(self):
        """Validate that only one of `time_window` or `relative_time` is set."""
        has_tw = self.time_window is not None
        has_rt = self.relative_time is not None
        if has_tw == has_rt:
            raise ValueError(
                "Exactly one of 'time_window' or 'relative_time' must be set")

        if has_tw:
            start, end = self.time_window  # type: ignore[misc]
            if not isinstance(start, datetime) or not isinstance(end, datetime):
                raise TypeError("time_window must be a tuple of datetimes")
            if end <= start:
                raise ValueError("time_window end must be after start")

        if has_rt:
            if not isinstance(self.relative_time, timedelta):
                raise TypeError("relative_time must be a timedelta")
            if self.relative_time.total_seconds() <= 0:
                raise ValueError("relative_time must be > 0 seconds")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        if self.time_window is not None:
            start, end = self.time_window
            return {
                "time_window": {
                    "start": start.astimezone(timezone.utc).isoformat(),
                    "end": end.astimezone(timezone.utc).isoformat(),
                }
            }
        else:
            # Represent relative_time as total seconds (int if whole seconds else float)
            # type: ignore[union-attr]
            secs = self.relative_time.total_seconds()
            secs_out: Union[int, float]
            secs_out = int(secs) if float(secs).is_integer() else float(secs)
            return {"relative_time": secs_out}
