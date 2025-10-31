import os
import sys
import time
import locale
import subprocess
from datetime import datetime


class SystemTimeDetector:
    '''System timezone and time format detection.'''

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # 1) Environment variable
        tz = os.environ.get('TZ')
        if tz:
            return tz

        # 2) Platform-specific approaches
        if sys.platform.startswith('win'):
            # Try PowerShell
            try:
                ps = subprocess.run(
                    ["powershell", "-NoProfile",
                        "-Command", "(Get-TimeZone).Id"],
                    capture_output=True, text=True, timeout=3
                )
                s = ps.stdout.strip()
                if s:
                    return s
            except Exception:
                pass
            # Try registry
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"System\CurrentControlSet\Control\TimeZoneInformation") as k:
                    try:
                        val, _ = winreg.QueryValueEx(k, "TimeZoneKeyName")
                        if val:
                            return val
                    except FileNotFoundError:
                        pass
                    try:
                        val, _ = winreg.QueryValueEx(k, "StandardName")
                        if val:
                            return val
                    except FileNotFoundError:
                        pass
            except Exception:
                pass
            # Fallback to abbreviation
            return time.tzname[0]

        # Non-Windows (Linux, macOS, etc.)
        # 3) timedatectl (Linux)
        try:
            td = subprocess.run(
                ["timedatectl", "show", "-p", "Timezone", "--value"],
                capture_output=True, text=True, timeout=2
            )
            s = td.stdout.strip()
            if s:
                return s
        except Exception:
            pass

        # 4) /etc/timezone (Debian/Ubuntu)
        try:
            if os.path.isfile("/etc/timezone"):
                with open("/etc/timezone", "r", encoding="utf-8", errors="ignore") as f:
                    s = f.readline().strip()
                    if s:
                        return s
        except Exception:
            pass

        # 5) /etc/localtime symlink -> .../zoneinfo/Region/City
        try:
            lt = "/etc/localtime"
            if os.path.exists(lt):
                # Resolve symlink chain
                real = os.path.realpath(lt)
                parts = real.split("/zoneinfo/")
                if len(parts) > 1 and parts[-1]:
                    return parts[-1]
                # On macOS, /etc/localtime might point into /var/db/timezone/zoneinfo/Region/City
                parts = real.split("/zoneinfo/")
                if len(parts) > 1 and parts[-1]:
                    return parts[-1]
        except Exception:
            pass

        # 6) macOS systemsetup (may require privileges, but try)
        if sys.platform == "darwin":
            try:
                ss = subprocess.run(
                    ["/usr/sbin/systemsetup", "-gettimezone"],
                    capture_output=True, text=True, timeout=3
                )
                out = ss.stdout.strip()
                # Output like: "Time Zone: America/Los_Angeles"
                if out and ":" in out:
                    tz = out.split(":", 1)[1].strip()
                    if tz:
                        return tz
            except Exception:
                pass

        # 7) Fallback to best-effort name
        try:
            # Try to use tzinfo name from local time
            tzinfo = datetime.now().astimezone().tzinfo
            name = getattr(tzinfo, "key", None) or getattr(
                tzinfo, "zone", None) or str(tzinfo)
            if name:
                return name
        except Exception:
            pass

        return time.tzname[0]

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        # Windows: check user time format from registry
        if sys.platform.startswith('win'):
            try:
                import winreg
                # Prefer user setting
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International") as k:
                    # sTimeFormat can be like "h:mm:ss tt" or "HH:mm:ss"
                    for name in ("sTimeFormat", "sShortTime"):
                        try:
                            fmt, _ = winreg.QueryValueEx(k, name)
                            if fmt:
                                if "H" in fmt:
                                    return "24h"
                                if "h" in fmt:
                                    return "12h"
                        except FileNotFoundError:
                            continue
                    # iTime: 0=12-hour, 1=24-hour
                    try:
                        itime, _ = winreg.QueryValueEx(k, "iTime")
                        if str(itime) == "1":
                            return "24h"
                        if str(itime) == "0":
                            return "12h"
                    except FileNotFoundError:
                        pass
            except Exception:
                pass

        # Locale-based heuristic for Unix/macOS or fallback for Windows
        try:
            current = locale.setlocale(locale.LC_TIME)
            try:
                locale.setlocale(locale.LC_TIME, "")
            except Exception:
                pass
            try:
                # If %p produces non-empty AM/PM designator, assume 12-hour
                test = datetime(2000, 1, 1, 13, 0, 0)
                ampm = test.strftime("%p")
                if ampm:
                    # Some locales may still include %p even with 24h, double-check format tokens if possible
                    try:
                        # On Unix, nl_langinfo may reveal %I or %H in T_FMT
                        if hasattr(locale, "nl_langinfo"):
                            t_fmt = locale.nl_langinfo(
                                getattr(locale, "T_FMT"))
                            if "%H" in t_fmt:
                                return "24h"
                            if "%I" in t_fmt:
                                return "12h"
                    except Exception:
                        pass
                    return "12h"
                else:
                    return "24h"
            finally:
                try:
                    locale.setlocale(locale.LC_TIME, current)
                except Exception:
                    pass
        except Exception:
            pass

        # Last resort: if timezone name includes AM/PM pattern is unknown; default to 24h
        return "24h"
