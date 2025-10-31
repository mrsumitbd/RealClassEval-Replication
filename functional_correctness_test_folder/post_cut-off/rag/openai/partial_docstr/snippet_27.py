
from __future__ import annotations

import datetime
from datetime import datetime as _datetime, timezone
from typing import Optional, Union

# The TimezoneHandler type is optional; if not provided we fall back to
# the standard library's timezone conversion.
try:
    from typing import Protocol

    class TimezoneHandler(Protocol):
        def to_utc(self, dt: _datetime) -> _datetime: ...
except Exception:
    TimezoneHandler = None  # pragma: no cover


class TimestampProcessor:
    """Unified timestamp parsing and processing utilities."""

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        """Initialize with optional timezone handler."""
        self.timezone_handler = timezone_handler

    def _to_utc(self, dt: _datetime) -> _datetime:
        """Convert a datetime to UTC, using the provided handler if available."""
        if dt.tzinfo is None:
            # Assume naive datetime is already UTC
            return dt.replace(tzinfo=timezone.utc).astimezone(timezone.utc)
        if self.timezone_handler is not None:
            return self.timezone_handler.to_utc(dt)
        return dt.astimezone(timezone.utc)

    def parse_timestamp(
        self, timestamp_value: Union[str, int, float, _datetime, None]
    ) -> Optional[_datetime]:
        """Parse timestamp from various formats to UTC datetime.

        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)

        Returns:
            Parsed UTC datetime or None if parsing fails
        """
        if timestamp_value is None:
            return None

        # If already a datetime instance
        if isinstance(timestamp_value, _datetime):
            return self._to_utc(timestamp_value)

        # If numeric (int or float), treat as epoch seconds
        if isinstance(timestamp_value, (int, float)):
            try:
                dt = _datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
                return dt
            except (OverflowError, OSError, ValueError):
                return None

        # If string, try multiple common formats
        if isinstance(timestamp_value, str):
            ts = timestamp_value.strip()
            if not ts:
                return None

            # ISO 8601 (with or without timezone)
            try:
                dt = _datetime.fromisoformat(ts)
                return self._to_utc(dt)
            except ValueError:
                pass

            # RFC 2822 / email format
            try:
                from email.utils import parsedate_to_datetime

                dt = parsedate_to_datetime(ts)
                return self._to_utc(dt)
            except Exception:
                pass

            # Common strptime patterns
            patterns = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%d/%m/%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S",
                "%Y-%m-%d",
                "%d-%b-%Y",
                "%b %d, %Y",
            ]
            for fmt in patterns:
                try:
                    dt = _datetime.strptime(ts, fmt)
                    return self._to_utc(dt)
                except ValueError:
                    continue

        # If none of the above worked, return None
        return None
