
import time
import platform


class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        if platform.system() == 'Windows':
            import _winreg as winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation")
            timezone, _ = winreg.QueryValueEx(key, "TimeZoneKeyName")
            winreg.CloseKey(key)
            return timezone
        else:
            import os
            return os.environ.get('TZ', time.tzname[time.daylight])

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        import locale
        locale.setlocale(locale.LC_TIME, '')
        time_format = locale.nl_langinfo(locale.T_FMT)
        if '%p' in time_format:
            return '12h'
        else:
            return '24h'
