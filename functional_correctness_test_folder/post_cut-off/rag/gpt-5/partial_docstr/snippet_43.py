import os
import sys
import time
import platform
import subprocess
import locale


class SystemTimeDetector:
    """System timezone and time format detection."""

    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        # 1) tzlocal if available
        try:
            import tzlocal  # type: ignore

            try:
                # tzlocal >= 3
                if hasattr(tzlocal, "get_localzone_name"):
                    name = tzlocal.get_localzone_name()
                    if name:
                        return str(name)
            except Exception:
                pass

            try:
                # tzlocal any version
                tz = tzlocal.get_localzone()
                name = getattr(tz, "key", None) or getattr(
                    tz, "zone", None) or str(tz)
                if name:
                    return str(name)
            except Exception:
                pass
        except Exception:
            pass

        # 2) TZ env var
        tz_env = os.environ.get("TZ")
        if tz_env:
            tz_str = tz_env
            if tz_str.startswith(":"):
                tz_str = tz_str[1:]
            if "/zoneinfo/" in tz_str:
                tz_str = tz_str.split("/zoneinfo/", 1)[1]
            elif os.path.isabs(tz_str) and os.path.exists(tz_str):
                try:
                    real = os.path.realpath(tz_str)
                    if "/zoneinfo/" in real:
                        tz_str = real.split("/zoneinfo/", 1)[1]
                except Exception:
                    pass
            if tz_str:
                return tz_str

        # 3) /etc/timezone (Debian/Ubuntu)
        try:
            with open("/etc/timezone", "r", encoding="utf-8") as f:
                value = f.read().strip()
                if value:
                    return value
        except Exception:
            pass

        # 4) /etc/localtime symlink or path containing zoneinfo
        for candidate in ("/etc/localtime", "/var/db/timezone/localtime"):
            try:
                if os.path.exists(candidate):
                    real = os.path.realpath(candidate)
                    if "/zoneinfo/" in real:
                        return real.split("/zoneinfo/", 1)[1]
            except Exception:
                pass

        # 5) macOS systemsetup
        if platform.system() == "Darwin":
            try:
                out = subprocess.check_output(
                    ["systemsetup", "-gettimezone"],
                    stderr=subprocess.STDOUT,
                    timeout=2,
                )
                text = out.decode(errors="ignore").strip()
                if ":" in text:
                    tz = text.split(":", 1)[1].strip()
                    if tz:
                        return tz
            except Exception:
                pass

        # 6) Windows registry
        if platform.system() == "Windows":
            try:
                import winreg  # type: ignore

                # Try TimeZoneKeyName first
                with winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation",
                ) as key:
                    try:
                        val, _ = winreg.QueryValueEx(key, "TimeZoneKeyName")
                        if val:
                            return str(val)
                    except FileNotFoundError:
                        pass
                    try:
                        stdname, _ = winreg.QueryValueEx(key, "StandardName")
                    except FileNotFoundError:
                        stdname = None

                if stdname:
                    # Map StandardName to time zone key name
                    with winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones",
                    ) as root:
                        i = 0
                        while True:
                            try:
                                subkey = winreg.EnumKey(root, i)
                            except OSError:
                                break
                            i += 1
                            try:
                                with winreg.OpenKey(root, subkey) as sk:
                                    try:
                                        std, _ = winreg.QueryValueEx(sk, "Std")
                                        if std == stdname:
                                            return subkey
                                    except FileNotFoundError:
                                        pass
                            except OSError:
                                pass
            except Exception:
                pass

        # 7) Fallback to tzname
        try:
            is_dst = bool(time.daylight) and time.localtime().tm_isdst > 0
            name = time.tzname[1 if is_dst else 0]
            if name:
                return name
        except Exception:
            pass

        # Final fallback
        return "UTC"

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        # 1) Windows registry
        if platform.system() == "Windows":
            try:
                import winreg  # type: ignore

                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, r"Control Panel\International"
                ) as key:
                    # Prefer explicit time format patterns
                    for value_name in ("sShortTime", "sTimeFormat"):
                        try:
                            fmt, _ = winreg.QueryValueEx(key, value_name)
                            if isinstance(fmt, str) and fmt:
                                # Windows uses 'H' for 24h and 'h' for 12h
                                if "H" in fmt:
                                    return "24h"
                                if "h" in fmt:
                                    return "12h"
                        except FileNotFoundError:
                            pass
                    # Fallback to iTime: 1=24h, 0=12h
                    try:
                        itime, _ = winreg.QueryValueEx(key, "iTime")
                        if str(itime) == "1":
                            return "24h"
                        if str(itime) == "0":
                            return "12h"
                    except FileNotFoundError:
                        pass
            except Exception:
                pass

        # 2) Locale-based detection (Unix/macOS and fallback for Windows)
        # Use user's default locale
        try:
            current = locale.setlocale(locale.LC_TIME)
        except Exception:
            current = None
        try:
            try:
                locale.setlocale(locale.LC_TIME, "")
            except Exception:
                pass

            # Prefer inspecting the format pattern if available
            if hasattr(locale, "nl_langinfo"):
                try:
                    fmt = locale.nl_langinfo(getattr(locale, "T_FMT"))
                    if isinstance(fmt, str):
                        if ("%I" in fmt) or ("%p" in fmt) or ("%r" in fmt):
                            return "12h"
                        if "%H" in fmt:
                            return "24h"
                except Exception:
                    pass

            # Fallback: presence of an AM/PM marker in current locale
            ampm = time.strftime("%p")
            if ampm:
                return "12h"
            return "24h"
        finally:
            if current is not None:
                try:
                    locale.setlocale(locale.LC_TIME, current)
                except Exception:
                    pass
