
import locale
import time


class SystemTimeDetector:
    """System timezone and time format detection."""
    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        return time.tzname[0]

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        time_format = locale.nl_langinfo(locale.T_FMT)
        return '12h' if '%I' in time_format or '%r' in time_format else '24h'
