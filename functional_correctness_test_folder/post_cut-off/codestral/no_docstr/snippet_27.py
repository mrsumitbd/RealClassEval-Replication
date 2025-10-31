
from typing import Optional, Union
from datetime import datetime


class TimestampProcessor:

    def __init__(self, timezone_handler: Optional['TimezoneHandler'] = None) -> None:
        self.timezone_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        if timestamp_value is None:
            return None
        if isinstance(timestamp_value, datetime):
            return timestamp_value
        if isinstance(timestamp_value, (int, float)):
            return datetime.fromtimestamp(timestamp_value)
        if isinstance(timestamp_value, str):
            try:
                return datetime.fromisoformat(timestamp_value)
            except ValueError:
                pass
        return None
