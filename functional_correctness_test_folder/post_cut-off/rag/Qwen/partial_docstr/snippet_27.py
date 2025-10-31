
from typing import Optional, Union
from datetime import datetime, timezone, timedelta
import pytz


class TimezoneHandler:
    def __init__(self, default_timezone: str = 'UTC'):
        self.default_timezone = pytz.timezone(default_timezone)

    def convert_to_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = self.default_timezone.localize(dt)
        return dt.astimezone(pytz.utc)


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
                dt = datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
                return dt
            except (OSError, OverflowError, ValueError):
                return None
        elif isinstance(timestamp_value, str):
            try:
                # Try to parse as ISO 8601 format
                dt = datetime.fromisoformat(timestamp_value)
                return self.timezone_handler.convert_to_utc(dt)
            except ValueError:
                try:
                    # Try to parse as a timestamp string
                    ts = float(timestamp_value)
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    return dt
                except (ValueError, OSError, OverflowError):
                    return None
        return None
