
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union

# Placeholder for the actual TimezoneHandler implementation.
# It is expected to provide a method `to_utc(dt: datetime) -> datetime`.


class TimezoneHandler:
    def to_utc(self, dt: datetime) -> datetime:
        """Convert a datetime to UTC. Override in actual implementation."""
        return dt.astimezone(timezone.utc)


class TimestampProcessor:
    """
    Utility class for parsing various timestamp representations into
    timezone-aware UTC datetime objects.
    """

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        """
        Initialize the processor with an optional timezone handler.

        :param timezone_handler: An object that can convert datetime objects
                                 to UTC. If None, the processor will use
                                 the built‑in conversion logic.
        """
        self.timezone_handler = timezone_handler

    def parse_timestamp(
        self, timestamp_value: Union[str, int, float, datetime, None]
    ) -> Optional[datetime]:
        """
        Parse a timestamp value into a timezone-aware UTC datetime.

        Supported input types:
            - str: ISO‑8601 or common date/time formats.
            - int/float: Unix epoch seconds (float may include milliseconds).
            - datetime: Returned as is (converted to UTC if necessary).
            - None: Returns None.

        :param timestamp_value: The value to parse.
        :return: A timezone-aware UTC datetime or None if parsing fails.
        """
        if timestamp_value is None:
            return None

        # If already a datetime instance
        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
        # If numeric (int or float) treat as epoch seconds
        elif isinstance(timestamp_value, (int, float)):
            try:
                dt = datetime.fromtimestamp(
                    float(timestamp_value), tz=timezone.utc)
            except (OverflowError, OSError, ValueError):
                return None
        # If string, attempt to parse
        elif isinstance(timestamp_value, str):
            dt = self._parse_string_timestamp(timestamp_value)
            if dt is None:
                return None
        else:
            # Unsupported type
            return None

        # Ensure datetime is timezone-aware
        if dt.tzinfo is None:
            # If a timezone handler is provided, use it to set tzinfo
            if self.timezone_handler:
                try:
                    dt = self.timezone_handler.to_utc(dt)
                except Exception:
                    # Fallback: assume naive datetime is UTC
                    dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.replace(tzinfo=timezone.utc)

        # Convert to UTC if not already
        if dt.tzinfo != timezone.utc:
            try:
                dt = dt.astimezone(timezone.utc)
            except Exception:
                return None

        return dt

    @staticmethod
    def _parse_string_timestamp(value: str) -> Optional[datetime]:
        """
        Attempt to parse a string into a datetime object using common formats.

        :param value: The string representation of the timestamp.
        :return: A datetime object or None if parsing fails.
        """
        # Try ISO 8601 with timezone
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass

        # Common fallback formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        # If all parsing attempts fail, return None
        return None
