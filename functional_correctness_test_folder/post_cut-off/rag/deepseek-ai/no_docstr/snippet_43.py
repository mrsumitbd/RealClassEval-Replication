
import time
import locale
from datetime import datetime


class SystemTimeDetector:
    """System timezone and time format detection."""
    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        return time.tzname[0] if time.tzname else "UTC"

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        time_format = datetime.now().strftime(
            '%p')  # Returns AM/PM if 12h format, empty if 24h
        return '12h' if time_format else '24h'
