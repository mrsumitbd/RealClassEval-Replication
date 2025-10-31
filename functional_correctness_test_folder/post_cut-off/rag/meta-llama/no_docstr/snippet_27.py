
from datetime import datetime
import dateutil.parser
import pytz
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
            if timestamp_value.tzinfo:
                return timestamp_value.astimezone(pytz.utc)
            else:
                if self.timezone_handler:
                    return self.timezone_handler.localize(timestamp_value).astimezone(pytz.utc)
                else:
                    return pytz.utc.localize(timestamp_value)

        if isinstance(timestamp_value, (int, float)):
            try:
                return datetime.fromtimestamp(timestamp_value, pytz.utc)
            except (OSError, OverflowError, ValueError):
                return None

        if isinstance(timestamp_value, str):
            try:
                dt = dateutil.parser.parse(timestamp_value)
                if dt.tzinfo:
                    return dt.astimezone(pytz.utc)
                else:
                    if self.timezone_handler:
                        return self.timezone_handler.localize(dt).astimezone(pytz.utc)
                    else:
                        return pytz.utc.localize(dt)
            except (ValueError, OverflowError):
                return None

        return None
