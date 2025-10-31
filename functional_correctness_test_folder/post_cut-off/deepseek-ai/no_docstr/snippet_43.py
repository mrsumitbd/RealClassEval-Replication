
import time
import locale


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        return time.tzname[0] if time.tzname else "UTC"

    @staticmethod
    def get_time_format() -> str:
        time_format = locale.nl_langinfo(locale.T_FMT)
        return time_format if time_format else "%H:%M:%S"
