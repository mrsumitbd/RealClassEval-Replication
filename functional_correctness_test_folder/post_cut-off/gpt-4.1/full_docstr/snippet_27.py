
from typing import Optional, Union
from datetime import datetime, timezone
import dateutil.parser


class TimezoneHandler:
    '''Dummy TimezoneHandler for demonstration.'''

    def to_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        '''Initialize with optional timezone handler.'''
        self.timezone_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        '''Parse timestamp from various formats to UTC datetime.
        Args:
            timestamp_value: Timestamp in various formats (str, int, float, datetime)
        Returns:
            Parsed UTC datetime or None if parsing fails
        '''
        if timestamp_value is None:
            return None

        dt = None

        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
        elif isinstance(timestamp_value, (int, float)):
            # Assume UNIX timestamp (seconds since epoch)
            try:
                dt = datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
            except Exception:
                return None
        elif isinstance(timestamp_value, str):
            try:
                dt = dateutil.parser.parse(timestamp_value)
            except Exception:
                return None
        else:
            return None

        # Ensure dt is timezone-aware and in UTC
        if dt.tzinfo is None:
            if self.timezone_handler:
                dt = self.timezone_handler.to_utc(dt)
            else:
                dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        return dt
