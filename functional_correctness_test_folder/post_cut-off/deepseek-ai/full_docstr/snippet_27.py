
from datetime import datetime
from typing import Optional, Union
from pytz import UTC
import dateutil.parser


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

        try:
            if isinstance(timestamp_value, (int, float)):
                parsed = datetime.fromtimestamp(timestamp_value, UTC)
            elif isinstance(timestamp_value, str):
                parsed = dateutil.parser.parse(timestamp_value)
                if parsed.tzinfo is not None:
                    parsed = parsed.astimezone(UTC)
                else:
                    parsed = parsed.replace(tzinfo=UTC)
            elif isinstance(timestamp_value, datetime):
                parsed = timestamp_value
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=UTC)
                else:
                    parsed = parsed.astimezone(UTC)
            else:
                return None
            return parsed
        except (ValueError, OverflowError, TypeError):
            return None
