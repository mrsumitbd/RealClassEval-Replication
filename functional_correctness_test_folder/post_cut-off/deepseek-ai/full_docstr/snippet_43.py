
import time
import locale
import pytz
from datetime import datetime


class SystemTimeDetector:
    '''System timezone and time format detection.'''
    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        return datetime.now(pytz.timezone('UTC')).astimezone().tzinfo.zone

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        time_format = locale.nl_langinfo(locale.T_FMT)
        if '%H' in time_format:
            return '24h'
        else:
            return '12h'
