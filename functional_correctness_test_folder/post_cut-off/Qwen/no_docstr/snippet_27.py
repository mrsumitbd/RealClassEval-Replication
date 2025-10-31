
from typing import Optional, Union
from datetime import datetime
import pytz


class TimezoneHandler:
    def __init__(self, timezone: str):
        self.timezone = timezone

    def convert_to_timezone(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        return dt.astimezone(pytz.timezone(self.timezone))


class TimestampProcessor:

    def __init__(self, timezone_handler: Optional[TimezoneHandler] = None) -> None:
        self.timezone_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        if timestamp_value is None:
            return None
        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
        elif isinstance(timestamp_value, (int, float)):
            dt = datetime.fromtimestamp(timestamp_value, pytz.utc)
        elif isinstance(timestamp_value, str):
            try:
                dt = datetime.fromisoformat(timestamp_value)
            except ValueError:
                try:
                    dt = datetime.strptime(
                        timestamp_value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return None
        else:
            return None

        if self.timezone_handler:
            dt = self.timezone_handler.convert_to_timezone(dt)

        return dt
