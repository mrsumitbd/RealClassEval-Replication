
from typing import Optional, Union
from datetime import datetime, timezone
import dateutil.parser


class TimestampProcessor:

    def __init__(self, timezone_handler: Optional['TimezoneHandler'] = None) -> None:
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

        # If already a datetime
        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
        # If int or float, treat as unix timestamp (seconds)
        elif isinstance(timestamp_value, (int, float)):
            try:
                dt = datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
            except Exception:
                return None
        # If string, try to parse
        elif isinstance(timestamp_value, str):
            try:
                dt = dateutil.parser.parse(timestamp_value)
            except Exception:
                return None
        else:
            return None

        # If timezone_handler is provided, use it to convert to UTC
        if self.timezone_handler is not None:
            try:
                dt = self.timezone_handler.to_utc(dt)
            except Exception:
                return None
        else:
            # If dt is naive, assume UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)

        return dt
