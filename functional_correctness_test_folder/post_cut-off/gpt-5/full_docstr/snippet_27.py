from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union, Any


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional[Any] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self.timezone_handler = timezone_handler

    def _apply_timezone(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            th = self.timezone_handler
            if th is not None:
                # Try common method names to make datetime aware or convert to UTC
                for method_name in ("to_utc", "localize", "make_aware", "attach", "convert"):
                    method = getattr(th, method_name, None)
                    if callable(method):
                        try:
                            aware = method(dt)
                            if isinstance(aware, datetime):
                                dt = aware
                                break
                        except Exception:
                            pass
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def _from_epoch(self, value: float) -> datetime:
        abs_v = abs(value)
        # Heuristics for unit detection
        if abs_v >= 1e18:
            # assume nanoseconds
            seconds = value / 1e9
        elif abs_v >= 1e15:
            # assume microseconds but very large; still handle as ns for safety
            seconds = value / 1e9
        elif abs_v >= 1e12:
            # milliseconds
            seconds = value / 1e3
        elif abs_v >= 1e10:
            # seconds but in the near future; still seconds
            seconds = value
        elif abs_v >= 1e6:
            # microseconds
            seconds = value / 1e6
        else:
            # seconds (including floats)
            seconds = value
        return datetime.fromtimestamp(seconds, tz=timezone.utc)

    def _parse_str(self, s: str) -> Optional[datetime]:
        s = s.strip()
        if not s:
            return None

        # Numeric epoch string (int or float)
        num = None
        try:
            if any(c in s for c in ".eE"):
                num = float(s)
            else:
                # Allow leading +/-
                if s.lstrip("+-").isdigit():
                    num = float(s)
        except Exception:
            num = None
        if num is not None:
            return self._from_epoch(num)

        # Handle Zulu time
        iso_candidate = s
        if s.endswith("Z") or s.endswith("z"):
            iso_candidate = s[:-1] + "+00:00"

        # Try fromisoformat for datetime
        for cand in (iso_candidate, s):
            try:
                dt = datetime.fromisoformat(cand)
                if isinstance(dt, datetime):
                    return self._apply_timezone(dt)
            except Exception:
                pass

        # Try common strptime patterns
        patterns = [
            "%Y-%m-%d %H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
        ]
        for pattern in patterns:
            try:
                dt = datetime.strptime(s, pattern)
                return self._apply_timezone(dt)
            except Exception:
                continue

        return None

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        '''Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        '''
        if timestamp_value is None:
            return None

        if isinstance(timestamp_value, datetime):
            return self._apply_timezone(timestamp_value)

        if isinstance(timestamp_value, (int, float)):
            try:
                return self._from_epoch(float(timestamp_value))
            except Exception:
                return None

        if isinstance(timestamp_value, str):
            return self._parse_str(timestamp_value)

        return None
