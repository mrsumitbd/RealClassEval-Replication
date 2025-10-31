
import time
import locale
import platform


class SystemTimeDetector:
    """System timezone and time format detection."""
    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        if platform.system() == 'Windows':
            import winreg
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation")
                timezone = winreg.QueryValueEx(key, "TimeZoneKeyName")[0]
                winreg.CloseKey(key)
                return timezone
            except WindowsError:
                return "UTC"
        else:
            try:
                with open('/etc/timezone', 'r') as f:
                    return f.read().strip()
            except FileNotFoundError:
                try:
                    tz = time.tzname[0]
                    return tz if tz else "UTC"
                except:
                    return "UTC"

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        try:
            # Try to get the locale's time format
            time_format = locale.nl_langinfo(locale.T_FMT)
            if '%I' in time_format or '%l' in time_format:
                return '12h'
            else:
                return '24h'
        except:
            # Fallback to checking the current time
            current_time = time.strftime('%H')
            if int(current_time) > 12:
                return '24h'
            else:
                return '12h'
