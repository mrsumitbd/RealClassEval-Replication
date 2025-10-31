
import pytz
from datetime import datetime


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        local_timezone = datetime.now(pytz.timezone('UTC')).astimezone().tzinfo
        return str(local_timezone)

    @staticmethod
    def get_time_format() -> str:
        current_time = datetime.now()
        time_format = "%H:%M:%S" if current_time.hour >= 12 else "%I:%M:%S"
        return time_format
