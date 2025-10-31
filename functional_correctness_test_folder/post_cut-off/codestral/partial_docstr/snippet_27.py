
from typing import Optional, Union
from datetime import datetime
import pytz


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

        if isinstance(timestamp_value, datetime):
            if timestamp_value.tzinfo is None:
                if self.timezone_handler is not None:
                    return self.timezone_handler.localize(timestamp_value)
                else:
                    return timestamp_value.replace(tzinfo=pytz.UTC)
            else:
                return timestamp_value.astimezone(pytz.UTC)

        if isinstance(timestamp_value, (int, float)):
            try:
                return datetime.fromtimestamp(timestamp_value, pytz.UTC)
            except (ValueError, OSError):
                return None

        if isinstance(timestamp_value, str):
            try:
                return datetime.strptime(timestamp_value, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
            except ValueError:
                try:
                    return datetime.strptime(timestamp_value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                except ValueError:
                    try:
                        return datetime.strptime(timestamp_value, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
                    except ValueError:
                        return None

        return None
