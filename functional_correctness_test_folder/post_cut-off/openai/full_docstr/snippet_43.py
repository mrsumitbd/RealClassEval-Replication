
import locale
import time
import datetime
try:
    from tzlocal import get_localzone_name
except ImportError:
    get_localzone_name = None


class SystemTimeDetector:
    '''System timezone and time format detection.'''

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # Try tzlocal first
        if get_localzone_name:
            try:
                tz = get_localzone_name()
                if tz:
                    return tz
            except Exception:
                pass

        # Fallback to time.tzname
        tzname = time.tzname[0]
        if tzname:
            return tzname

        # Last resort: use datetime
        try:
            tzinfo = datetime.datetime.now().astimezone().tzinfo
            if tzinfo:
                return tzinfo.tzname(None)
        except Exception:
            pass

        return 'UTC'

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        # Use locale to get AM/PM marker
        try:
            locale.setlocale(locale.LC_TIME, '')
        except Exception:
            pass

        am_pm = time.strftime('%p')
        if am_pm and am_pm.strip():
            return '12h'
        return '24h'
