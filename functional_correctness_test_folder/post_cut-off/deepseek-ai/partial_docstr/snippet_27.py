
from datetime import datetime
from typing import Union, Optional
from pytz import UTC
import dateutil.parser


class TimestampProcessor:

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
                parsed_dt = datetime.fromtimestamp(timestamp_value, UTC)
            elif isinstance(timestamp_value, str):
                parsed_dt = dateutil.parser.parse(timestamp_value)
                if parsed_dt.tzinfo is None:
                    parsed_dt = parsed_dt.replace(tzinfo=UTC)
                else:
                    parsed_dt = parsed_dt.astimezone(UTC)
            elif isinstance(timestamp_value, datetime):
                if timestamp_value.tzinfo is None:
                    parsed_dt = timestamp_value.replace(tzinfo=UTC)
                else:
                    parsed_dt = timestamp_value.astimezone(UTC)
            else:
                return None

            return parsed_dt
        except (ValueError, OverflowError, TypeError, AttributeError):
            return None
