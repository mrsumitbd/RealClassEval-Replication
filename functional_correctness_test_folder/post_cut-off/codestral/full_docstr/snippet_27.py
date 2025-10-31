
from typing import Optional, Union
from datetime import datetime
import pytz


class TimezoneHandler:
    '''Handles timezone conversions.'''

    def __init__(self, timezone: str = 'UTC') -> None:
        self.timezone = pytz.timezone(timezone)

    def convert_to_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = self.timezone.localize(dt)
        return dt.astimezone(pytz.utc)


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self.timezone_handler = timezone_handler if timezone_handler is not None else TimezoneHandler()

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
            return self.timezone_handler.convert_to_utc(timestamp_value)

        if isinstance(timestamp_value, (int, float)):
            try:
                return self.timezone_handler.convert_to_utc(datetime.fromtimestamp(timestamp_value))
            except (ValueError, OSError):
                return None

        if isinstance(timestamp_value, str):
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%z'):
                try:
                    dt = datetime.strptime(timestamp_value, fmt)
                    return self.timezone_handler.convert_to_utc(dt)
                except ValueError:
                    continue
            try:
                dt = datetime.fromisoformat(timestamp_value)
                return self.timezone_handler.convert_to_utc(dt)
            except ValueError:
                pass

        return None
