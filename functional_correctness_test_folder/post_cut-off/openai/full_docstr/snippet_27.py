
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union

# Placeholder for the external TimezoneHandler type.
# In real usage, import the actual class.


class TimezoneHandler:
    def to_utc(self, dt: datetime) -> datetime:
        """Convert a datetime to UTC. Implementation is user‑defined."""
        raise NotImplementedError


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self.timezone_handler = timezone_handler

    def parse_timestamp(
        self, timestamp_value: Union[str, int, float, datetime, None]
    ) -> Optional[datetime]:
        '''Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        '''
        if timestamp_value is None:
            return None

        # Handle datetime objects
        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
            if dt.tzinfo is None:
                # Assume naive datetime is already UTC
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt

        # Handle numeric timestamps (seconds or milliseconds)
        if isinstance(timestamp_value, (int, float)):
            try:
                # If value is large, assume milliseconds
                if abs(timestamp_value) > 1e12:
                    ts = timestamp_value / 1000.0
                else:
                    ts = timestamp_value
                dt = datetime.utcfromtimestamp(ts).replace(tzinfo=timezone.utc)
                return dt
            except (OverflowError, OSError, ValueError):
                return None

        # Handle string timestamps
        if isinstance(timestamp_value, str):
            ts_str = timestamp_value.strip()
            # Try ISO 8601 format
            try:
                dt = datetime.fromisoformat(ts_str)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt.astimezone(timezone.utc)
                return dt
            except ValueError:
                pass

            # Try common datetime formats
            common_formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
                "%d-%m-%Y",
                "%m-%d-%Y",
            ]
            for fmt in common_formats:
                try:
                    dt = datetime.strptime(ts_str, fmt)
                    dt = dt.replace(tzinfo=timezone.utc)
                    return dt
                except ValueError:
                    continue

            # If a timezone handler is provided, try to parse with it
            if self.timezone_handler:
                try:
                    dt = self.timezone_handler.to_utc(
                        datetime.fromisoformat(ts_str))
                    return dt
                except Exception:
                    pass

        # If all parsing attempts fail, return None
        return None
