
import time
import locale
from datetime import datetime


class SystemTimeDetector:
    """System timezone and time format detection."""
    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        return datetime.now().astimezone().tzname()

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        time_format = time.strftime("%H:%M")
        if time_format.startswith(('0', '1', '2')) and ':' in time_format:
            return '24h' if int(time_format.split(':')[0]) >= 0 else '12h'
        return '12h'
