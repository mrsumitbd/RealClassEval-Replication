
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union

# A minimal placeholder for TimezoneHandler.  In real usage this would be
# replaced by the actual implementation that knows how to convert a
# datetime to UTC.


class TimezoneHandler:
    def to_utc(self, dt: datetime) -> datetime:
        """Convert a timezone-aware datetime to UTC."""
        if dt.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware")
        return dt.astimezone(timezone.utc)


class TimestampProcessor:
    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        """Initialize with optional timezone handler."""
        self.timezone_handler = timezone_handler

    def parse_timestamp(
        self, timestamp_value: Union[str, int, float, datetime, None]
    ) -> Optional[datetime]:
        """
        Parse timestamp from various formats to UTC datetime.

        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)

        Returns:
            Parsed UTC datetime or None if parsing fails
        """
        if timestamp_value is None:
            return None

        # Handle datetime objects
        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
            if dt.tzinfo is None:
                # If a timezone handler is provided, use it to interpret the naive datetime
                if self.timezone_handler is not None:
                    try:
                        dt = self.timezone_handler.to_utc(dt)
                    except Exception:
                        # Fallback: assume naive datetime is already UTC
                        dt = dt.replace(tzinfo=timezone.utc)
                else:
                    # Assume naive datetime is UTC
                    dt = dt.replace(tzinfo=timezone.utc)
            else:
                # Convert to UTC
                dt = dt.astimezone(timezone.utc)
            return dt

        # Handle numeric timestamps (epoch seconds)
        if isinstance(timestamp_value, (int, float)):
            try:
                dt = datetime.utcfromtimestamp(
                    timestamp_value).replace(tzinfo=timezone.utc)
                return dt
            except (OverflowError, OSError, ValueError):
                return None

        # Handle string timestamps
        if isinstance(timestamp_value, str):
            ts = timestamp_value.strip()
            # Try ISO 8601 format first
            try:
                dt = datetime.fromisoformat(ts)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt.astimezone(timezone.utc)
                return dt
            except ValueError:
                pass

            # Try common datetime formats
            for fmt in (
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
            ):
                try:
                    dt = datetime.strptime(ts, fmt)
                    dt = dt.replace(tzinfo=timezone.utc)
                    return dt
                except ValueError:
                    continue

            # If all parsing attempts fail, return None
            return None

        # Unsupported type
        return None
