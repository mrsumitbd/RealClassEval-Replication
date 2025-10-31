
import time
import locale
import datetime


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        return time.tzname[0]

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        try:
            locale.setlocale(locale.LC_ALL, '')
            time_format = locale.nl_langinfo(locale.T_FMT)
            if '%I' in time_format or '%r' in time_format:
                return '12h'
            else:
                return '24h'
        except Exception:
            # Fallback for systems where locale.nl_langinfo is not available
            now = datetime.datetime.now()
            time_str = now.strftime('%X')
            if 'AM' in time_str or 'PM' in time_str:
                return '12h'
            elif now.hour > 12:
                return '24h'
            else:
                # Try formatting with 12-hour clock
                time_str_12h = now.strftime('%I:%M:%S %p')
                if time_str == time_str_12h[:-3]:  # Compare without AM/PM
                    return '24h'
                else:
                    return '12h'
