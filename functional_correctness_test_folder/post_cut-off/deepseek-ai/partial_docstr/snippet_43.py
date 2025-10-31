
import time
import locale


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        return time.tzname[0] if time.tzname else "UTC"

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        time_format = locale.nl_langinfo(locale.T_FMT)
        if "%I" in time_format or "%p" in time_format:
            return "12h"
        else:
            return "24h"
