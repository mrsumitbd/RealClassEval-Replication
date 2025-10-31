import time
import locale
import os
import sys


class SystemTimeDetector:
    '''System timezone and time format detection.'''

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # Try using time.tzname
        if hasattr(time, 'tzname'):
            # On most systems, time.tzname[0] is the local timezone name
            return time.tzname[time.daylight] if time.daylight and time.localtime().tm_isdst else time.tzname[0]
        # Fallback to environment variable
        tz = os.environ.get('TZ')
        if tz:
            return tz
        # Fallback to /etc/timezone (Linux)
        if sys.platform.startswith('linux'):
            try:
                with open('/etc/timezone') as f:
                    return f.read().strip()
            except Exception:
                pass
        # Fallback to UTC
        return 'UTC'

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        # Try to get locale time format
        try:
            locale.setlocale(locale.LC_TIME, '')
            fmt = locale.nl_langinfo(locale.T_FMT)
        except Exception:
            fmt = '%H:%M:%S'
        # If %I (12-hour) is in the format, it's 12h, else 24h
        if '%I' in fmt or '%p' in fmt:
            return '12h'
        return '24h'
