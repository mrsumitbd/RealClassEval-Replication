
from datetime import datetime
from typing import Optional, Union


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

        if isinstance(timestamp_value, datetime):
            if self.timezone_handler:
                return self.timezone_handler.to_utc(timestamp_value)
            return timestamp_value

        try:
            if isinstance(timestamp_value, (int, float)):
                return datetime.utcfromtimestamp(timestamp_value)

            if isinstance(timestamp_value, str):
                try:
                    timestamp_float = float(timestamp_value)
                    return datetime.utcfromtimestamp(timestamp_float)
                except ValueError:
                    formats = [
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%dT%H:%M:%S',
                        '%Y-%m-%d %H:%M:%S.%f',
                        '%Y-%m-%dT%H:%M:%S.%f',
                        '%Y-%m-%d'
                    ]
                    for fmt in formats:
                        try:
                            dt = datetime.strptime(timestamp_value, fmt)
                            if self.timezone_handler:
                                return self.timezone_handler.to_utc(dt)
                            return dt
                        except ValueError:
                            continue
        except (ValueError, OverflowError, OSError):
            pass

        return None
