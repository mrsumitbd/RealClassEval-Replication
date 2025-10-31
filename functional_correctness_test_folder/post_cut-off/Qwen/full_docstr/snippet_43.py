
import time
import locale


class SystemTimeDetector:
    '''System timezone and time format detection.'''
    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        return time.tzname[time.daylight]

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        current_locale = locale.getlocale(locale.LC_TIME)
        time_format = locale.nl_langinfo(locale.T_FMT)
        locale.setlocale(locale.LC_TIME, current_locale)
        if '%p' in time_format:
            return '12h'
        else:
            return '24h'
