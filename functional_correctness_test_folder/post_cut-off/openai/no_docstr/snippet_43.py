
import datetime
import locale
import time


class SystemTimeDetector:
    @staticmethod
    def get_timezone() -> str:
        """
        Return the system's local timezone name.
        """
        try:
            tz_name = datetime.datetime.now().astimezone().tzinfo.tzname(None)
            if tz_name:
                return tz_name
        except Exception:
            pass
        # Fallback to time module
        return time.tzname[0] if time.tzname else "UTC"

    @staticmethod
    def get_time_format() -> str:
        """
        Return the locale's time format string.
        """
        try:
            # locale.nl_langinfo is available on Unix; fallback to default
            return locale.nl_langinfo(locale.T_FMT)
        except Exception:
            # Default to a common 24‑hour format
            return "%H:%M:%S"
