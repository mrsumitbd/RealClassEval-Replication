
import time
import locale
import os
import sys


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # Try to get from environment variable first
        tz = os.environ.get('TZ')
        if tz:
            return tz
        # Try to get from time.tzname
        if hasattr(time, 'tzname'):
            # On most systems, time.tzname[0] is the local timezone name
            return time.tzname[time.daylight]
        # Fallback: try /etc/timezone (Linux)
        try:
            with open('/etc/timezone') as f:
                return f.read().strip()
        except Exception:
            pass
        # Fallback: try /etc/localtime symlink (Linux)
        try:
            if os.path.islink('/etc/localtime'):
                tz_path = os.readlink('/etc/localtime')
                if 'zoneinfo' in tz_path:
                    return tz_path.split('zoneinfo/')[-1]
        except Exception:
            pass
        # Fallback: unknown
        return 'Unknown'

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        # Try to get locale time format
        try:
            locale.setlocale(locale.LC_TIME, '')
            time_fmt = locale.nl_langinfo(locale.T_FMT)
            # If %I (12-hour) is in the format, it's 12h, else 24h
            if '%I' in time_fmt:
                return '12h'
            elif '%H' in time_fmt:
                return '24h'
        except Exception:
            pass
        # Fallback: try to format time and check for AM/PM
        try:
            t = time.strftime('%X')
            if 'AM' in t or 'PM' in t or 'am' in t or 'pm' in t:
                return '12h'
        except Exception:
            pass
        # Fallback: default to 24h
        return '24h'
