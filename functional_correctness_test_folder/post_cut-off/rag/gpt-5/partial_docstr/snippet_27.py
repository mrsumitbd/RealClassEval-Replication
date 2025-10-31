from datetime import datetime, timezone, tzinfo, date, time as dtime
from typing import Optional, Union, Any
from email.utils import parsedate_to_datetime
import re


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional['TimezoneHandler'] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self._tz_handler: Optional[Any] = timezone_handler

    def _get_default_tz(self) -> tzinfo:
        h = self._tz_handler
        if h is None:
            return timezone.utc
        # Direct tzinfo
        if isinstance(h, tzinfo):
            return h
        # tzinfo attribute
        tzi = getattr(h, 'tzinfo', None)
        if isinstance(tzi, tzinfo):
            return tzi
        # common provider methods
        for meth in ('get_default_timezone', 'get_timezone'):
            if hasattr(h, meth):
                try:
                    tz = getattr(h, meth)()
                    if isinstance(tz, tzinfo):
                        return tz
                except Exception:
                    pass
        return timezone.utc

    def _localize_naive(self, dt: datetime) -> datetime:
        if dt.tzinfo is not None:
            return dt
        h = self._tz_handler
        # pytz/localize-style handlers
        if h is not None and hasattr(h, 'localize'):
            try:
                localized = h.localize(dt)  # type: ignore[attr-defined]
                if isinstance(localized, datetime) and localized.tzinfo is not None:
                    return localized
            except Exception:
                pass
        tz = self._get_default_tz()
        # Some tz providers may also provide a localize method
        if hasattr(tz, 'localize'):
            try:
                localized = tz.localize(dt)  # type: ignore[attr-defined]
                if isinstance(localized, datetime) and localized.tzinfo is not None:
                    return localized
            except Exception:
                pass
        return dt.replace(tzinfo=tz)

    def _from_unix(self, value: float) -> Optional[datetime]:
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc)
        except (OSError, OverflowError, ValueError):
            return None

    def _numeric_to_seconds(self, value: Union[int, float]) -> float:
        v = float(value)
        av = abs(v)
        if av >= 1e18:      # ns
            return v / 1e9
        if av >= 1e15:      # µs
            return v / 1e6
        if av >= 1e12:      # ms
            return v / 1e3
        return v            # s

    def _parse_string(self, s: str) -> Optional[datetime]:
        s = s.strip()
        if not s:
            return None
        # numeric string (epoch)
        if re.fullmatch(r'[+-]?\d+(\.\d+)?', s):
            try:
                v = float(s)
            except ValueError:
                return None
            secs = self._numeric_to_seconds(v)
            return self._from_unix(secs)

        # Normalize common UTC markers
        if s.endswith('Z'):
            s_norm = s[:-1] + '+00:00'
        elif s.upper().endswith(' UTC'):
            s_norm = s[: -4] + '+00:00'
        else:
            s_norm = s

        # Try ISO 8601
        try:
            dt = datetime.fromisoformat(s_norm)
            if isinstance(dt, datetime):
                if dt.tzinfo is None:
                    dt = self._localize_naive(dt)
                return dt.astimezone(timezone.utc)
        except Exception:
            pass

        # Try date-only
        try:
            d = date.fromisoformat(s)
            dt = datetime.combine(d, dtime.min)
            dt = self._localize_naive(dt)
            return dt.astimezone(timezone.utc)
        except Exception:
            pass

        # RFC 2822 / email date
        try:
            dt = parsedate_to_datetime(s)
            if dt is not None:
                if dt.tzinfo is None:
                    dt = self._localize_naive(dt)
                return dt.astimezone(timezone.utc)
        except Exception:
            pass

        # Common strptime patterns
        patterns = (
            '%Y-%m-%d %H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S%z',
            '%Y/%m/%d %H:%M:%S',
            '%Y-%m-%d %H:%M%z',
            '%Y-%m-%d %H:%M',
            '%Y/%m/%d %H:%M%z',
            '%Y/%m/%d %H:%M',
            '%d %b %Y %H:%M:%S %z',
            '%d %b %Y %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d',
        )
        for pat in patterns:
            try:
                dt = datetime.strptime(s, pat)
                if dt.tzinfo is None:
                    dt = self._localize_naive(dt)
                return dt.astimezone(timezone.utc)
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
                dt = self._localize_naive(dt)
            try:
                return dt.astimezone(timezone.utc)
            except Exception:
                return None

        if isinstance(timestamp_value, (int, float)):
            secs = self._numeric_to_seconds(timestamp_value)
            return self._from_unix(secs)

        if isinstance(timestamp_value, str):
            return self._parse_string(timestamp_value)

        return None
