
import time
import locale


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        return time.tzname[time.daylight] if time.daylight and time.localtime().tm_isdst > 0 else time.tzname[0]

    @staticmethod
    def get_time_format() -> str:
        locale.setlocale(locale.LC_TIME, '')
        time_format = locale.nl_langinfo(locale.T_FMT)
        if '%H' in time_format:
            return '24-hour'
        elif '%I' in time_format or '%l' in time_format:
            return '12-hour'
        else:
            # Fallback: check formatted time string for AM/PM
            formatted = time.strftime(time_format)
            if 'AM' in formatted or 'PM' in formatted or 'am' in formatted or 'pm' in formatted:
                return '12-hour'
            else:
                return '24-hour'
