
import locale
import time


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        return time.tzname[0]

    @staticmethod
    def get_time_format() -> str:
        time_format = '%H:%M:%S' if locale.nl_langinfo(
            locale.T_FMT) == '%T' else '%I:%M:%S %p'
        return time_format
