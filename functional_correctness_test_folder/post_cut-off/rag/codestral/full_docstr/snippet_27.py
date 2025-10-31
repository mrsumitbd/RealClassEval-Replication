
from typing import Optional, Union
from datetime import datetime
import pytz


class TimezoneHandler:
    '''Timezone handling utilities.'''
    pass


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self.timezone_handler = timezone_handler or TimezoneHandler()

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        '''Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        '''
        if timestamp_value is None:
            return None

        if isinstance(timestamp_value, datetime):
            if timestamp_value.tzinfo is None:
                return timestamp_value.replace(tzinfo=pytz.UTC)
            return timestamp_value.astimezone(pytz.UTC)

        if isinstance(timestamp_value, (int, float)):
            try:
                return datetime.fromtimestamp(timestamp_value, pytz.UTC)
            except (ValueError, OSError):
                return None

        if isinstance(timestamp_value, str):
            try:
                # Try parsing as ISO format
                return datetime.fromisoformat(timestamp_value).astimezone(pytz.UTC)
            except ValueError:
                pass

            try:
                # Try parsing as Unix timestamp
                return datetime.fromtimestamp(float(timestamp_value), pytz.UTC)
            except (ValueError, OSError):
                pass

            try:
                # Try parsing with timezone handler
                return self.timezone_handler.parse(timestamp_value)
            except (ValueError, AttributeError):
                pass

        return None
