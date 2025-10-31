from datetime import datetime, timezone, tzinfo
from typing import Optional, Union, TYPE_CHECKING
import re
from email.utils import parsedate_to_datetime

if TYPE_CHECKING:
    from typing import Any as TimezoneHandler  # placeholder for type checking


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional['TimezoneHandler'] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self._tz_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        '''Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        '''
        if timestamp_value is None:
            return None

        try:
            if isinstance(timestamp_value, datetime):
                return self._to_utc(self._localize_if_naive(timestamp_value))

            if isinstance(timestamp_value, (int, float)):
                dt = self._from_numeric(timestamp_value)
                return self._to_utc(dt) if dt else None

            if isinstance(timestamp_value, str):
                s = timestamp_value.strip()
                if not s:
                    return None

                # Numeric string (epoch)
                if re.fullmatch(r'[+-]?\d+(\.\d+)?', s):
                    num = float(s) if '.' in s else int(s)
                    dt = self._from_numeric(num)
                    return self._to_utc(dt) if dt else None

                # ISO-like normalization: Z -> +00:00; +HHMM -> +HH:MM
                iso_candidate = re.sub(r'Z$', '+00:00', s, flags=re.IGNORECASE)
                iso_candidate = re.sub(
                    r'([+-]\d{2})(\d{2})$', r'\1:\2', iso_candidate)

                # Try fromisoformat first
                try:
                    dt = datetime.fromisoformat(iso_candidate)
                    return self._to_utc(self._localize_if_naive(dt))
                except Exception:
                    pass

                # Try RFC2822/RFC1123 via email.utils
                try:
                    dt = parsedate_to_datetime(s)
                    return self._to_utc(self._localize_if_naive(dt))
                except Exception:
                    pass

                # Try common strptime patterns (both space and 'T')
                base = s.replace('T', ' ')
                patterns = (
                    '%Y-%m-%d %H:%M:%S.%f%z',
                    '%Y-%m-%d %H:%M:%S%z',
                    '%Y-%m-%d %H:%M:%S.%f',
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d',
                )
                for fmt in patterns:
                    try:
                        dt = datetime.strptime(base, fmt)
                        return self._to_utc(self._localize_if_naive(dt))
                    except Exception:
                        continue

                return None

            return None
        except Exception:
            return None

    # Helpers

    def _from_numeric(self, value: Union[int, float]) -> Optional[datetime]:
        # Floats are assumed to be seconds.
        if isinstance(value, float):
            try:
                return datetime.fromtimestamp(value, tz=timezone.utc)
            except Exception:
                return None

        # Ints: infer unit by digit length
        try:
            n = int(value)
        except Exception:
            return None

        absn = abs(n)
        digits = len(str(absn)) if absn != 0 else 1

        try:
            if digits <= 10:
                # seconds
                return datetime.fromtimestamp(n, tz=timezone.utc)
            elif digits <= 13:
                # milliseconds
                return datetime.fromtimestamp(n / 1_000, tz=timezone.utc)
            elif digits <= 16:
                # microseconds
                seconds = n // 1_000_000
                micros = n % 1_000_000
                base = datetime.fromtimestamp(seconds, tz=timezone.utc)
                return base.replace(microsecond=micros)
            elif digits <= 19:
                # nanoseconds
                seconds = n // 1_000_000_000
                nanos = n % 1_000_000_000
                base = datetime.fromtimestamp(seconds, tz=timezone.utc)
                return base.replace(microsecond=(nanos // 1000))
            else:
                # Fallback to seconds
                return datetime.fromtimestamp(n, tz=timezone.utc)
        except Exception:
            return None

    def _to_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def _localize_if_naive(self, dt: datetime) -> datetime:
        if dt.tzinfo is not None:
            return dt
        tz = self._get_handler_tz()
        if tz is None:
            # Assume UTC if no handler/unknown tz
            return dt.replace(tzinfo=timezone.utc)
        # If handler exposes 'localize' (e.g., pytz-style)
        localize = getattr(self._tz_handler, 'localize', None)
        if callable(localize):
            try:
                return localize(dt)  # type: ignore[misc]
            except Exception:
                pass
        # Otherwise, attach tzinfo directly
        try:
            return dt.replace(tzinfo=tz)
        except Exception:
            return dt.replace(tzinfo=timezone.utc)

    def _get_handler_tz(self) -> Optional[tzinfo]:
        h = self._tz_handler
        if h is None:
            return None
        # Common access patterns
        for attr in ('tzinfo', 'default_timezone'):
            tz = getattr(h, attr, None)
            if isinstance(tz, tzinfo):
                return tz
        for meth in ('get_timezone', 'get_default_timezone'):
            fn = getattr(h, meth, None)
            if callable(fn):
                try:
                    tz = fn()
                    if isinstance(tz, tzinfo):
                        return tz
                except Exception:
                    continue
        return None
