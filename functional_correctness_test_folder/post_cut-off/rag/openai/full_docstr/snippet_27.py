
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union

# A minimal protocol for a timezone handler.  The real implementation may
# provide more sophisticated conversion logic.


class TimezoneHandler:
    def to_utc(self, dt: datetime) -> datetime:
        """Convert a datetime to UTC."""
        raise NotImplementedError


class TimestampProcessor:
    """Unified timestamp parsing and processing utilities."""

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        """Initialize with optional timezone handler."""
        self.timezone_handler = timezone_handler

    def parse_timestamp(
        self,
        timestamp_value: Union[str, int, float, datetime, None],
    ) -> Optional[datetime]:
        """Parse timestamp from various formats to UTC datetime.

        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)

        Returns:
            Parsed UTC datetime or None if parsing fails
        """
        if timestamp_value is None:
            return None

        # 1. datetime instance
        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
            if dt.tzinfo is None:
                # Assume naive datetime is already UTC
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt

        # 2. int or float – treat as POSIX timestamp (seconds)
        if isinstance(timestamp_value, (int, float)):
            try:
                return datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
            except (OverflowError, OSError, ValueError):
                return None

        # 3. string – try ISO format first, then common patterns
        if isinstance(timestamp_value, str):
            ts_str = timestamp_value.strip()
            # Try ISO 8601
            try:
                dt = datetime.fromisoformat(ts_str)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt.astimezone(timezone.utc)
                return dt
            except ValueError:
                pass

            # Common fallback formats
            for fmt in (
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
                "%m/%d/%Y %H:%M:%S",
                "%m/%d/%Y",
            ):
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
