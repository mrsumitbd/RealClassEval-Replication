
from datetime import datetime
import dateutil.parser
from typing import Optional, Union
from dateutil.tz import tzutc


class TimezoneHandler:
    # Assuming TimezoneHandler is defined elsewhere
    pass


class TimestampProcessor:
    """Unified timestamp parsing and processing utilities."""

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
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
                return timestamp_value.astimezone(tzutc())
            else:
                # Assuming local timezone if no timezone info is available
                # You might need to adjust this based on your specific requirements
                return timestamp_value.replace(tzinfo=self.timezone_handler.get_local_timezone() if self.timezone_handler else None).astimezone(tzutc())

        try:
            if isinstance(timestamp_value, (int, float)):
                # Assuming Unix timestamp
                return datetime.fromtimestamp(timestamp_value, tz=tzutc())

            if isinstance(timestamp_value, str):
                # Try to parse the string using dateutil parser
                dt = dateutil.parser.parse(timestamp_value)
                if dt.tzinfo:
                    return dt.astimezone(tzutc())
                else:
                    # Assuming local timezone if no timezone info is available
                    # You might need to adjust this based on your specific requirements
                    return dt.replace(tzinfo=self.timezone_handler.get_local_timezone() if self.timezone_handler else None).astimezone(tzutc())

        except (ValueError, OverflowError):
            # If parsing fails, return None
            return None

        return None
