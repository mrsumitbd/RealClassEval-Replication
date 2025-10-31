
import locale
import datetime


class SystemTimeDetector:
    """System timezone and time format detection."""
    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        try:
            return datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
        except Exception:
            return "Unknown"

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        try:
            locale_time_format = locale.nl_langinfo(locale.T_FMT)
            return '12h' if '%I' in locale_time_format or '%r' in locale_time_format else '24h'
        except Exception:
            return '24h'
