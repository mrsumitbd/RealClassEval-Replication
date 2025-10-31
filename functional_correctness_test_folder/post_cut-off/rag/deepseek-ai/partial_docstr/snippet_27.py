
from datetime import datetime
from typing import Optional, Union


class TimestampProcessor:
    """Unified timestamp parsing and processing utilities."""

    def __init__(self, timezone_handler: Optional['TimezoneHandler'] = None) -> None:
        """Initialize with optional timezone handler."""
        self.timezone_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        """Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        """
        if timestamp_value is None:
            return None

        if isinstance(timestamp_value, datetime):
            if self.timezone_handler:
                return self.timezone_handler.to_utc(timestamp_value)
            return timestamp_value

        if isinstance(timestamp_value, (int, float)):
            try:
                parsed_datetime = datetime.utcfromtimestamp(timestamp_value)
                return parsed_datetime
            except (ValueError, OSError):
                return None

        if isinstance(timestamp_value, str):
            try:
                # Try parsing as ISO format
                parsed_datetime = datetime.fromisoformat(timestamp_value)
                if self.timezone_handler:
                    return self.timezone_handler.to_utc(parsed_datetime)
                return parsed_datetime
            except ValueError:
                try:
                    # Try parsing as Unix timestamp string
                    timestamp_float = float(timestamp_value)
                    parsed_datetime = datetime.utcfromtimestamp(
                        timestamp_float)
                    return parsed_datetime
                except (ValueError, OSError):
                    return None

        return None
