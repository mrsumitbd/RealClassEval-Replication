class SystemTimeDetector:
    import os
    import sys
    import subprocess
    import locale
    import time as _time
    import platform
    from pathlib import Path

    @staticmethod
    def _run_cmd(cmd):
        try:
            out = SystemTimeDetector.subprocess.check_output(
                cmd, stderr=SystemTimeDetector.subprocess.DEVNULL, text=True
            )
            return out.strip()
        except Exception:
            return None

    @staticmethod
    def _get_timezone_from_tzlocal():
        try:
            from tzlocal import get_localzone_name  # type: ignore
            name = get_localzone_name()
            if name:
                return name
        except Exception:
            pass
        try:
            from tzlocal import get_localzone  # type: ignore
            tz = get_localzone()
            # Some tz implementations provide a key attribute or zone
            name = getattr(tz, "key", None) or getattr(tz, "zone", None)
            if name:
                return name
        except Exception:
            pass
        return None

    @staticmethod
    def _get_timezone_from_etc_localtime():
        try:
            path = SystemTimeDetector.Path("/etc/localtime")
            if path.is_symlink():
                target = path.resolve()
                parts = str(target).split("/zoneinfo/")
                if len(parts) > 1:
                    return parts[-1]
            # Fallback: try /etc/timezone file (Debian/Ubuntu)
            tzfile = SystemTimeDetector.Path("/etc/timezone")
            if tzfile.exists():
                content = tzfile.read_text(
                    encoding="utf-8", errors="ignore").strip()
                if content:
                    return content
            # Try timedatectl
            out = SystemTimeDetector._run_cmd(["timedatectl"])
            if out:
                for line in out.splitlines():
                    line = line.strip()
                    if line.lower().startswith("time zone:"):
                        # Example: "Time zone: Europe/Berlin (CEST, +0200)"
                        parts = line.split(": ", 1)
                        if len(parts) == 2:
                            tz_part = parts[1].split(" ", 1)[0]
                            if tz_part and "/" in tz_part:
                                return tz_part
        except Exception:
            pass
        return None

    @staticmethod
    def _get_timezone_from_macos():
        # systemsetup -gettimezone
        out = SystemTimeDetector._run_cmd(["systemsetup", "-gettimezone"])
        if out:
            # Output like: "Time Zone: Europe/Berlin"
            if ":" in out:
                tz = out.split(":", 1)[1].strip()
                if tz:
                    return tz
        # macOS also links /etc/localtime
        return SystemTimeDetector._get_timezone_from_etc_localtime()

    @staticmethod
    def _get_timezone_from_windows():
        # tzutil /g returns Windows time zone ID (e.g., "Pacific Standard Time")
        out = SystemTimeDetector._run_cmd(["tzutil", "/g"])
        if out:
            return out
        return None

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # Try tzlocal if available
        tz = SystemTimeDetector._get_timezone_from_tzlocal()
        if tz:
            return tz

        system = SystemTimeDetector.platform.system().lower()
        if system == "windows":
            tz = SystemTimeDetector._get_timezone_from_windows()
            if tz:
                return tz
        elif system == "darwin":
            tz = SystemTimeDetector._get_timezone_from_macos()
            if tz:
                return tz
        else:
            tz = SystemTimeDetector._get_timezone_from_etc_localtime()
            if tz:
                return tz

        # Fallbacks
        try:
            # Python's datetime may provide a name
            import datetime as _dt

            name = _dt.datetime.now().astimezone().tzinfo
            tzname = getattr(name, "key", None) or getattr(
                name, "zone", None) or str(name)
            if tzname and tzname not in ("None", "UTC+00:00"):
                return tzname
        except Exception:
            pass

        try:
            # time.tzname gives abbreviations; last resort
            tzname = SystemTimeDetector._time.tzname[0] or SystemTimeDetector._time.tzname[1]
            if tzname:
                return tzname
        except Exception:
            pass

        return "UTC"

    @staticmethod
    def _detect_time_format_from_locale():
        try:
            # Use LC_TIME without changing global locale permanently
            fmt = SystemTimeDetector.locale.nl_langinfo(
                SystemTimeDetector.locale.T_FMT)
            if "%H" in fmt:
                return "24h"
            if "%I" in fmt or "%r" in fmt:
                return "12h"
        except Exception:
            pass
        # Heuristic using %p (AM/PM)
        try:
            ampm = SystemTimeDetector._time.strftime("%p")
            if ampm:
                return "12h"
        except Exception:
            pass
        return None

    @staticmethod
    def _detect_time_format_windows():
        try:
            import winreg  # type: ignore

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International") as key:
                # iTime: 0 for 12-hour, 1 for 24-hour
                iTime, _ = winreg.QueryValueEx(key, "iTime")
                if str(iTime) == "1":
                    return "24h"
                if str(iTime) == "0":
                    return "12h"
                # sTimeFormat may contain 'H' vs 'h'
                try:
                    sTimeFormat, _ = winreg.QueryValueEx(key, "sTimeFormat")
                    if "H" in sTimeFormat:
                        return "24h"
                    if "h" in sTimeFormat:
                        return "12h"
                except Exception:
                    pass
        except Exception:
            pass
        return None

    @staticmethod
    def _detect_time_format_macos():
        # Check user preferences
        out = SystemTimeDetector._run_cmd(
            ["defaults", "read", "-g", "AppleICUForce24HourTime"])
        if out is not None:
            if out.strip() in ("1", "YES", "true", "True"):
                return "24h"
            if out.strip() in ("0", "NO", "false", "False"):
                # If explicitly false, may indicate 12h unless locale dictates otherwise
                pass
        out = SystemTimeDetector._run_cmd(
            ["defaults", "read", "-g", "AppleICUForce12HourTime"])
        if out is not None:
            if out.strip() in ("1", "YES", "true", "True"):
                return "12h"
        return None

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        system = SystemTimeDetector.platform.system().lower()
        if system == "windows":
            fmt = SystemTimeDetector._detect_time_format_windows()
            if fmt:
                return fmt
        elif system == "darwin":
            fmt = SystemTimeDetector._detect_time_format_macos()
            if fmt:
                return fmt

        fmt = SystemTimeDetector._detect_time_format_from_locale()
        if fmt:
            return fmt

        # Fallback heuristic: if AM/PM present in formatted time, assume 12h
        try:
            sample = SystemTimeDetector._time.strftime("%X")
            if any(token.lower() in sample.lower() for token in ("am", "pm")):
                return "12h"
        except Exception:
            pass

        return "24h"
