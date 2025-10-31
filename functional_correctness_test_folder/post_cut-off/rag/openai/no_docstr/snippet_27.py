
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union

# The TimestampProcessor can optionally use a custom timezone handler.
# The handler is expected to provide a method `to_utc(dt: datetime) -> datetime`.
# If no handler is supplied, the built‑in `datetime.astimezone(timezone.utc)` is used.


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional[object] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self.timezone_handler = timezone_handler

    def _to_utc(self, dt: datetime) -> datetime:
        '''Convert a datetime to UTC using the configured handler or the standard library.'''
        if self.timezone_handler is not None:
            # Assume the handler has a `to_utc` method.
            try:
                return self.timezone_handler.to_utc(dt)
            except Exception:
                # Fall back to the standard conversion if the handler fails.
                pass
        # If dt is naive, assume it is already UTC.
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def parse_timestamp(
        self,
        timestamp_value: Union[str, int, float, datetime, None]
    ) -> Optional[datetime]:
        '''Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        '''
        if timestamp_value is None:
            return None

        # 1. datetime instance
        if isinstance(timestamp_value, datetime):
            return self._to_utc(timestamp_value)

        # 2. int or float – treat as POSIX timestamp (seconds)
        if isinstance(timestamp_value, (int, float)):
            try:
                # If the value is too large, assume milliseconds.
                if abs(timestamp_value) > 1e12:
                    ts = timestamp_value / 1000.0
                else:
                    ts = timestamp_value
                dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                return dt
            except Exception:
                return None

        # 3. string – try several common formats
        if isinstance(timestamp_value, str):
            ts_str = timestamp_value.strip()
            if not ts_str:
                return None

            # a) ISO 8601 (Python 3.7+)
            try:
                dt = datetime.fromisoformat(ts_str)
                return self._to_utc(dt)
            except Exception:
                pass

            # b) Common datetime formats without timezone
            common_formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
                "%d/%m/%Y %H:%M:%S",
                "%d-%m-%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S",
                "%m-%d-%Y %H:%M:%S",
            ]
            for fmt in common_formats:
                try:
                    dt = datetime.strptime(ts_str, fmt)
                    return self._to_utc(dt)
                except Exception:
                    continue

            # c) Try parsing with timezone offset if present
            #    e.g., "2023-08-15 13:45:30+02:00"
            try:
                # Split offset manually
                if '+' in ts_str or '-' in ts_str[10:]:
                    # Find the last '+' or '-' after the date part
                    for sep in ('+', '-'):
                        if sep in ts_str[10:]:
                            parts = ts_str.rsplit(sep, 1)
                            if len(parts) == 2:
                                base, offset = parts
                                base = base.strip()
                                offset = sep + offset.strip()
                                dt = datetime.strptime(
                                    base, "%Y-%m-%d %H:%M:%S")
                                # Parse offset
                                off_hours, off_minutes = map(
                                    int, offset[1:].split(':'))
                                delta = timezone(
                                    timedelta(hours=off_hours, minutes=off_minutes))
                                dt = dt.replace(tzinfo=delta)
                                return self._to_utc(dt)
                # If we reach here, parsing failed
            except Exception:
                pass

        # If all parsing attempts fail, return None
        return None
