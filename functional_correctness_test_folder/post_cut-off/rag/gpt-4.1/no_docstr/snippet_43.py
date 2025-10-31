import time
import locale
import os
import sys


class SystemTimeDetector:
    '''System timezone and time format detection.'''

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # Try using time.tzname and time.daylight
        if time.daylight and time.localtime().tm_isdst:
            tz = time.tzname[1]
        else:
            tz = time.tzname[0]
        # Try to get Olson database name if possible
        # On Unix, /etc/localtime is often a symlink to zoneinfo
        if hasattr(time, 'tzname'):
            try:
                if sys.platform.startswith('linux') or sys.platform == 'darwin':
                    tzpath = os.path.realpath('/etc/localtime')
                    zoneinfo = '/usr/share/zoneinfo/'
                    if tzpath.startswith(zoneinfo):
                        return tzpath[len(zoneinfo):]
            except Exception:
                pass
        return tz

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        try:
            locale.setlocale(locale.LC_TIME, '')
        except Exception:
            pass
        t_fmt = locale.nl_langinfo(locale.T_FMT) if hasattr(
            locale, 'nl_langinfo') and hasattr(locale, 'T_FMT') else '%H:%M:%S'
        # Check for %I (12-hour) or %H (24-hour)
        if '%I' in t_fmt or '%p' in t_fmt:
            return '12h'
        return '24h'
