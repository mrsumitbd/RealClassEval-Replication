
import time
import locale
import os
import sys


class SystemTimeDetector:
    '''System timezone and time format detection.'''
    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # Try to get from TZ environment variable
        tz_env = os.environ.get('TZ')
        if tz_env:
            return tz_env

        # Try to get from time.tzname
        if hasattr(time, 'tzname'):
            # On most systems, time.tzname[0] is the standard timezone name
            return time.tzname[0]

        # On Unix, try /etc/timezone
        if sys.platform.startswith('linux'):
            try:
                with open('/etc/timezone') as f:
                    return f.read().strip()
            except Exception:
                pass

        # On macOS, try systemsetup
        if sys.platform == 'darwin':
            try:
                import subprocess
                output = subprocess.check_output(
                    ['systemsetup', '-gettimezone'], stderr=subprocess.DEVNULL)
                return output.decode().strip().split(':')[-1].strip()
            except Exception:
                pass

        # Fallback
        return 'Unknown'

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        # Try to get locale time format
        try:
            locale.setlocale(locale.LC_TIME, '')
            time_format = locale.nl_langinfo(locale.T_FMT)
            # If %I (12-hour) is in the format, it's 12h, else if %H (24-hour), it's 24h
            if '%I' in time_format:
                return '12h'
            elif '%H' in time_format:
                return '24h'
        except Exception:
            pass

        # Fallback: check formatted time string for AM/PM
        t = time.strftime('%X')
        if 'AM' in t or 'PM' in t or 'am' in t or 'pm' in t:
            return '12h'
        else:
            return '24h'
