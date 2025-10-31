
import time
import platform
from datetime import datetime


class SystemTimeDetector:
    '''System timezone and time format detection.'''
    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        if platform.system() == 'Windows':
            import pytz
            from tzlocal import get_localzone
            return get_localzone().zone
        else:
            return time.tzname[time.daylight]

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        # Create a test datetime object
        test_time = datetime.now()
        # Format the time in 12-hour format and 24-hour format
        time_12h = test_time.strftime('%I:%M %p')
        time_24h = test_time.strftime('%H:%M')
        # Check the length and presence of AM/PM to determine the format
        if 'AM' in time_12h or 'PM' in time_12h:
            return '12h'
        else:
            return '24h'
