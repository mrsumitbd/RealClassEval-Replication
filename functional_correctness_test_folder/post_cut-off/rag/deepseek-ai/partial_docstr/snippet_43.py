
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
        time_format = locale.nl_langinfo(locale.T_FMT)
        if "%p" in time_format:
            return "12h"
        else:
            return "24h"
