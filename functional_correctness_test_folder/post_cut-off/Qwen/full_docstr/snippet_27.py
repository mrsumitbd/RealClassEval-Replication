
from typing import Optional, Union
from datetime import datetime, timezone
import pytz


class TimezoneHandler:
    def convert_to_utc(self, dt: datetime) -> datetime:
        return dt.astimezone(timezone.utc)


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
        if isinstance(timestamp_value, datetime):
            return self.timezone_handler.convert_to_utc(timestamp_value)
        elif isinstance(timestamp_value, (int, float)):
            try:
                return datetime.fromtimestamp(timestamp_value, timezone.utc)
            except (OSError, OverflowError, ValueError):
                return None
        elif isinstance(timestamp_value, str):
            try:
                dt = datetime.fromisoformat(timestamp_value)
                if dt.tzinfo is None:
                    dt = pytz.utc.localize(dt)
                return self.timezone_handler.convert_to_utc(dt)
            except ValueError:
                try:
                    dt = datetime.strptime(
                        timestamp_value, '%Y-%m-%d %H:%M:%S')
                    if dt.tzinfo is None:
                        dt = pytz.utc.localize(dt)
                    return self.timezone_handler.convert_to_utc(dt)
                except ValueError:
                    return None
        return None
