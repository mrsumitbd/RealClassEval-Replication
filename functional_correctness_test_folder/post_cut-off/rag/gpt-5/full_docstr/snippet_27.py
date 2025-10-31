from __future__ import annotations

import re
from datetime import datetime, timezone, tzinfo
from typing import Optional, Union, Any

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:
    ZoneInfo = None  # type: ignore

try:
    from dateutil import parser as dateutil_parser  # type: ignore
except Exception:
    dateutil_parser = None  # type: ignore


class TimestampProcessor:
    """Unified timestamp parsing and processing utilities."""

    def __init__(self, timezone_handler: Optional['TimezoneHandler'] = None) -> None:
        """Initialize with optional timezone handler."""
        self._tz_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        """Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        """
        if timestamp_value is None:
            return None

        try:
            if isinstance(timestamp_value, datetime):
                return self._to_utc(timestamp_value)

            if isinstance(timestamp_value, (int, float)):
                dt = self._from_epoch(float(timestamp_value))
                return self._to_utc(dt)

            if isinstance(timestamp_value, str):
                s = timestamp_value.strip()
                if not s:
                    return None

                # Numeric string -> epoch
                if re.fullmatch(r'[+-]?\d+(\.\d+)?', s):
                    dt = self._from_epoch(float(s))
                    return self._to_utc(dt)

                # Try ISO-8601 first
                dt = self._parse_iso8601(s)
                if dt is not None:
                    return self._to_utc(dt)

                # Try python-dateutil if available
                if dateutil_parser is not None:
                    try:
                        dt = dateutil_parser.isoparse(s)
                    except Exception:
                        try:
                            dt = dateutil_parser.parse(s)
                        except Exception:
                            dt = None
                    if dt is not None:
                        return self._to_utc(dt)

                # Try a few common strptime patterns
                dt = self._parse_with_patterns(s)
                if dt is not None:
                    return self._to_utc(dt)

            return None
        except Exception:
            return None

    # Internal utilities

    def _from_epoch(self, value: float) -> datetime:
        # Detect unit by magnitude (absolute value)
        av = abs(value)
        # nanoseconds
        if av >= 1e17:
            seconds = value / 1e9
        # microseconds
        elif av >= 1e14:
            seconds = value / 1e6
        # milliseconds
        elif av >= 1e11:
            seconds = value / 1e3
        else:
            seconds = value
        return datetime.fromtimestamp(seconds, tz=timezone.utc)

    def _parse_iso8601(self, s: str) -> Optional[datetime]:
        # Normalize Z suffix
        s_norm = s
        if s_norm.endswith('Z') or s_norm.endswith('z'):
            s_norm = s_norm[:-1] + '+00:00'

        # Attempt fromisoformat
        try:
            dt = datetime.fromisoformat(s_norm)
            return dt
        except Exception:
            pass

        # Try replacing space with T if needed
        if ' ' in s_norm and 'T' not in s_norm:
            try:
                dt = datetime.fromisoformat(s_norm.replace(' ', 'T'))
                return dt
            except Exception:
                pass

        return None

    def _parse_with_patterns(self, s: str) -> Optional[datetime]:
        patterns = (
            '%Y-%m-%d %H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S.%f%z',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S%z',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d',
        )
        for pat in patterns:
            try:
                dt = datetime.strptime(s, pat)
                return dt
            except Exception:
                continue
        return None

    def _to_utc(self, dt: datetime) -> datetime:
        # If a handler provides a to_utc, prefer it
        handler = self._tz_handler
        if handler is not None and hasattr(handler, 'to_utc'):
            try:
                out = handler.to_utc(dt)  # type: ignore[attr-defined]
                if isinstance(out, datetime):
                    # Ensure timezone-aware and in UTC
                    if out.tzinfo is None:
                        return out.replace(tzinfo=timezone.utc)
                    return out.astimezone(timezone.utc)
            except Exception:
                pass

        # If naive, attach default timezone
        if dt.tzinfo is None:
            tz = self._get_default_tz()
            dt = dt.replace(tzinfo=tz)

        return dt.astimezone(timezone.utc)

    def _get_default_tz(self) -> tzinfo:
        # Attempt to extract tzinfo from handler
        handler = self._tz_handler
        if handler is not None:
            # get_default_timezone()
            tz = self._call_if_exists(handler, 'get_default_timezone')
            if self._is_tzinfo(tz):
                return tz  # type: ignore[return-value]

            # get_timezone()
            tz = self._call_if_exists(handler, 'get_timezone')
            if self._is_tzinfo(tz):
                return tz  # type: ignore[return-value]

            # tzinfo attribute
            tz = getattr(handler, 'tzinfo', None)
            if self._is_tzinfo(tz):
                return tz  # type: ignore[return-value]

            # timezone attribute
            tz = getattr(handler, 'timezone', None)
            if self._is_tzinfo(tz):
                return tz  # type: ignore[return-value]

            # If a string like 'UTC' or 'Europe/Berlin' is provided
            for attr in ('default_timezone', 'tz', 'name'):
                tz_val = getattr(handler, attr, None)
                tzinfo_obj = self._tzinfo_from_any(tz_val)
                if tzinfo_obj is not None:
                    return tzinfo_obj

        return timezone.utc

    def _tzinfo_from_any(self, val: Any) -> Optional[tzinfo]:
        if self._is_tzinfo(val):
            return val  # type: ignore[return-value]
        if isinstance(val, str):
            if val.upper() in ('UTC', 'Z', 'GMT'):
                return timezone.utc
            if ZoneInfo is not None:
                try:
                    return ZoneInfo(val)
                except Exception:
                    return None
        return None

    @staticmethod
    def _is_tzinfo(val: Any) -> bool:
        return isinstance(val, tzinfo)

    @staticmethod
    def _call_if_exists(obj: Any, name: str) -> Any:
        if hasattr(obj, name):
            meth = getattr(obj, name)
            try:
                return meth() if callable(meth) else meth
            except Exception:
                return None
        return None
