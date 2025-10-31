
from typing import Optional, Union
from datetime import datetime


class TimestampProcessor:

    def __init__(self, timezone_handler: Optional['TimezoneHandler'] = None) -> None:
        self.timezone_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        if timestamp_value is None:
            return None
        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
        elif isinstance(timestamp_value, (int, float)):
            try:
                dt = datetime.fromtimestamp(timestamp_value)
            except Exception:
                return None
        elif isinstance(timestamp_value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d"):
                try:
                    dt = datetime.strptime(timestamp_value, fmt)
                    break
                except ValueError:
                    continue
            else:
                try:
                    # Try ISO format
                    dt = datetime.fromisoformat(timestamp_value)
                except Exception:
                    return None
        else:
            return None

        if self.timezone_handler is not None:
            dt = self.timezone_handler.localize(dt)
        return dt
