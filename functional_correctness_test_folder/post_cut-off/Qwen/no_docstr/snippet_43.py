
import datetime
import time


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        return time.tzname[time.daylight]

    @staticmethod
    def get_time_format() -> str:
        return "%Y-%m-%d %H:%M:%S"
