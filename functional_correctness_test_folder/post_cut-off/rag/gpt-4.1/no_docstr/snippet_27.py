from datetime import datetime, timezone
from typing import Optional, Union


class TimestampProcessor:
    '''Unified timestamp parsing and processing utilities.'''

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

        if isinstance(timestamp_value, datetime):
            dt = timestamp_value
        elif isinstance(timestamp_value, (int, float)):
            try:
                dt = datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
            except Exception:
                return None
        elif isinstance(timestamp_value, str):
            # Try ISO format first
            try:
                dt = datetime.fromisoformat(timestamp_value)
            except Exception:
                # Try common formats
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y"):
                    try:
                        dt = datetime.strptime(timestamp_value, fmt)
                        break
                    except Exception:
                        continue
                if dt is None:
                    return None
        else:
            return None

        # Attach timezone if missing
        if dt.tzinfo is None:
            if self.timezone_handler is not None:
                dt = self.timezone_handler.localize(dt)
            else:
                dt = dt.replace(tzinfo=timezone.utc)
        # Convert to UTC
        return dt.astimezone(timezone.utc)
