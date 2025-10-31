from __future__ import annotations

from datetime import datetime, timezone, tzinfo
from typing import Optional, Union, Any
import re
from email.utils import parsedate_to_datetime


class TimestampProcessor:

    def __init__(self, timezone_handler: Optional[Any] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self._tz_handler = timezone_handler

    def _apply_timezone_handler(self, dt: datetime) -> datetime:
        if dt.tzinfo is not None:
            return dt
        h = self._tz_handler
        if h is None:
            return dt.replace(tzinfo=timezone.utc)
        # Try common method names to attach/localize timezone
        if hasattr(h, "to_utc"):
            try:
                res = h.to_utc(dt)
                if isinstance(res, datetime) and res.tzinfo is not None:
                    return res.astimezone(timezone.utc)
            except Exception:
                pass
        if hasattr(h, "localize"):
            try:
                res = h.localize(dt)
                if isinstance(res, datetime) and res.tzinfo is not None:
                    return res.astimezone(timezone.utc)
            except Exception:
                pass
        if hasattr(h, "attach_tz"):
            try:
                res = h.attach_tz(dt)
                if isinstance(res, datetime) and res.tzinfo is not None:
                    return res.astimezone(timezone.utc)
            except Exception:
                pass
        if hasattr(h, "tzinfo") and isinstance(getattr(h, "tzinfo"), tzinfo):
            try:
                return dt.replace(tzinfo=h.tzinfo).astimezone(timezone.utc)
            except Exception:
                pass
        # Fallback: assume naive is UTC
        return dt.replace(tzinfo=timezone.utc)

    def _from_numeric_timestamp(self, value: Union[int, float]) -> Optional[datetime]:
        try:
            v = float(value)
        except (TypeError, ValueError):
            return None
        av = abs(v)
        # Heuristics for unit (seconds/milliseconds/microseconds)
        if av >= 1e14:
            v /= 1e6  # microseconds to seconds
        elif av >= 1e11:
            v /= 1e3  # milliseconds to seconds
        try:
            return datetime.fromtimestamp(v, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None

    def _from_string(self, s: str) -> Optional[datetime]:
        s = s.strip()
        if not s:
            return None

        # Numeric-like strings
        num_match = re.fullmatch(r"[+-]?\d+(?:\.\d+)?", s)
        if num_match:
            try:
                if "." in s:
                    return self._from_numeric_timestamp(float(s))
                else:
                    return self._from_numeric_timestamp(int(s))
            except Exception:
                pass

        # ISO 8601 handling (including 'Z')
        iso_candidate = s
        if s.endswith("Z") and ("+" not in s and "-" in s[-6:] is False):
            iso_candidate = s[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(iso_candidate)
            if dt.tzinfo is None:
                dt = self._apply_timezone_handler(dt)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt
        except Exception:
            pass

        # RFC 2822 / email date formats
        try:
            dt2 = parsedate_to_datetime(s)
            if isinstance(dt2, datetime):
                if dt2.tzinfo is None:
                    dt2 = self._apply_timezone_handler(dt2)
                else:
                    dt2 = dt2.astimezone(timezone.utc)
                return dt2
        except Exception:
            pass

        # Fallback custom common formats
        fmts = [
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S%z",
            "%Y/%m/%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y/%m/%d",
        ]
        for fmt in fmts:
            try:
                dt3 = datetime.strptime(s, fmt)
                if dt3.tzinfo is None:
                    dt3 = self._apply_timezone_handler(dt3)
                else:
                    dt3 = dt3.astimezone(timezone.utc)
                return dt3
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
            dt = timestamp_value
            if dt.tzinfo is None:
                dt = self._apply_timezone_handler(dt)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt

        if isinstance(timestamp_value, (int, float)):
            return self._from_numeric_timestamp(timestamp_value)

        if isinstance(timestamp_value, str):
            return self._from_string(timestamp_value)

        return None
