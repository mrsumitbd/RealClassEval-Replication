
from typing import Optional, Union
from datetime import datetime, timezone
import dateutil.parser


class TimezoneHandler:
    def convert_to_utc(self, dt: datetime) -> datetime:
        return dt.astimezone(timezone.utc)


class TimestampProcessor:

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        self.timezone_handler = timezone_handler or TimezoneHandler()

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        if timestamp_value is None:
            return None
        if isinstance(timestamp_value, datetime):
            return self.timezone_handler.convert_to_utc(timestamp_value)
        try:
            if isinstance(timestamp_value, (int, float)):
                dt = datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
            else:
                dt = dateutil.parser.isoparse(timestamp_value)
            return self.timezone_handler.convert_to_utc(dt)
        except (ValueError, OverflowError, TypeError):
            return None
