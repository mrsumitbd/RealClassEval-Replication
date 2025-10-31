import os
import sys
import subprocess
import locale
from datetime import datetime


class SystemTimeDetector:
    """System timezone and time format detection."""

    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        # 1) Try TZ environment variable
        tz_env = os.environ.get('TZ')
        if tz_env:
            tz = SystemTimeDetector._extract_iana_from_any(tz_env)
            if tz:
                return tz

        system = sys.platform
        # 2) OS-specific detection
        if system.startswith('linux') or system.startswith('freebsd') or system.startswith('aix'):
            tz = SystemTimeDetector._detect_timezone_unix()
            if tz:
                return tz
        elif system == 'darwin':
            tz = SystemTimeDetector._detect_timezone_macos()
            if tz:
                return tz
            # Fallback to Unix-like methods if macOS method failed
            tz = SystemTimeDetector._detect_timezone_unix()
            if tz:
                return tz
        elif system.startswith('win'):
            tz = SystemTimeDetector._detect_timezone_windows()
            if tz:
                return tz

        # 3) Try to get key from datetime tzinfo (may expose ZoneInfo.key)
        try:
            tzinfo = datetime.now().astimezone().tzinfo
            key = getattr(tzinfo, 'key', None)
            if isinstance(key, str) and key:
                return key
        except Exception:
            pass

        # 4) Fallback
        return 'UTC'

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        # Windows: use registry settings
        if sys.platform.startswith('win'):
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Control Panel\International') as k:
                    # iTime: 0 = 12-hour, 1 = 24-hour
                    try:
                        itime, _ = winreg.QueryValueEx(k, 'iTime')
                        if str(itime).strip() == '1':
                            return '24h'
                        if str(itime).strip() == '0':
                            return '12h'
                    except FileNotFoundError:
                        pass
                    # sShortTime: contains H (24h) or h + tt (12h)
                    for name in ('sShortTime', 'sTimeFormat'):
                        try:
                            fmt, _ = winreg.QueryValueEx(k, name)
                            if isinstance(fmt, str):
                                if 'H' in fmt:  # 24-hour usually uses H or HH
                                    return '24h'
                                if 'h' in fmt:  # 12-hour usually uses h or hh
                                    return '12h'
                        except FileNotFoundError:
                            continue
            except Exception:
                pass
            # Fallback: inspect formatted time
            return SystemTimeDetector._infer_12h_or_24h_by_format()

        # macOS specific hint (optional)
        if sys.platform == 'darwin':
            try:
                # AppleICUForce24HourTime: 1 forces 24-hour, 0 or missing respects locale
                out = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleICUForce24HourTime'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=0.5,
                )
                val = out.stdout.strip()
                if val == '1':
                    return '24h'
                if val == '0':
                    # fall through to locale detection
                    pass
            except Exception:
                pass

        # POSIX: use locale to inspect T_FMT
        try:
            old = locale.setlocale(locale.LC_TIME)
        except Exception:
            old = None

        try:
            try:
                locale.setlocale(locale.LC_TIME, '')
            except Exception:
                pass

            if hasattr(locale, 'nl_langinfo'):
                try:
                    fmt = locale.nl_langinfo(locale.T_FMT)
                    if isinstance(fmt, str):
                        if '%I' in fmt or '%p' in fmt:
                            return '12h'
                        if '%H' in fmt:
                            return '24h'
                except Exception:
                    pass
        finally:
            if old:
                try:
                    locale.setlocale(locale.LC_TIME, old)
                except Exception:
                    pass

        # Fallback: inspect formatted time string for a 13:00 case
        return SystemTimeDetector._infer_12h_or_24h_by_format()

    # ----------------- Helpers -----------------

    @staticmethod
    def _infer_12h_or_24h_by_format() -> str:
        try:
            # Format a known 13:05 time to see if "13" appears
            dt = datetime(2000, 1, 1, 13, 5, 0)
            s = dt.strftime('%X')
            # Extract first group of digits (hour)
            digits = ''.join(ch for ch in s if ch.isdigit() or ch in ' :.-/')
            # Try to parse hour at start
            hour_str = ''
            for ch in digits:
                if ch.isdigit():
                    hour_str += ch
                else:
                    break
            if hour_str:
                try:
                    hour = int(hour_str)
                    if hour >= 13:
                        return '24h'
                    # If hour is 1 for 13:xx, likely 12h
                    return '12h'
                except ValueError:
                    pass
        except Exception:
            pass
        # Default to 24h if undecidable
        return '24h'

    @staticmethod
    def _extract_iana_from_any(value: str) -> str | None:
        if not value:
            return None
        v = value.strip()
        if not v:
            return None
        # Strip leading colon, common in POSIX TZ strings
        if v.startswith(':'):
            v = v[1:]

        # If it's an absolute path pointing into zoneinfo, extract tail
        lower = v.lower()
        if 'zoneinfo' in lower:
            try:
                # Normalize path and extract substring after "zoneinfo/"
                norm = os.path.realpath(v)
                parts = norm.replace('\\', '/').split('/zoneinfo/', 1)
                if len(parts) == 2:
                    candidate = parts[1].lstrip('/')
                    if candidate:
                        return candidate
            except Exception:
                pass

        # If it resembles an IANA key (has slash)
        if '/' in v and not v.startswith('/'):
            return v

        # Common UTC variants
        if v in ('UTC', 'Etc/UTC', 'GMT', 'Z', 'UCT'):
            return 'Etc/UTC'

        # Last resort: if it points to a file that links into zoneinfo
        if os.path.exists(v):
            try:
                real = os.path.realpath(v)
                parts = real.replace('\\', '/').split('/zoneinfo/', 1)
                if len(parts) == 2:
                    candidate = parts[1].lstrip('/')
                    if candidate:
                        return candidate
            except Exception:
                pass

        return None

    @staticmethod
    def _detect_timezone_unix() -> str | None:
        # /etc/timezone (Debian/Ubuntu)
        for path in ('/etc/timezone', '/var/db/timezone/zoneinfo', '/etc/TZ'):
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        line = f.read().strip()
                        tz = SystemTimeDetector._extract_iana_from_any(line)
                        if tz:
                            return tz
            except Exception:
                pass

        # /etc/localtime symlink or file pointing into zoneinfo
        try:
            if os.path.exists('/etc/localtime'):
                real = os.path.realpath('/etc/localtime')
                tz = SystemTimeDetector._extract_iana_from_any(real)
                if tz:
                    return tz
        except Exception:
            pass

        # RHEL/CentOS
        for path in ('/etc/sysconfig/clock', '/etc/conf.d/clock'):
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith('#'):
                                continue
                            if line.startswith('ZONE=') or line.startswith('TIMEZONE='):
                                value = line.split('=', 1)[
                                    1].strip().strip('"\'')
                                tz = SystemTimeDetector._extract_iana_from_any(
                                    value)
                                if tz:
                                    return tz
            except Exception:
                pass

        return None

    @staticmethod
    def _detect_timezone_macos() -> str | None:
        # systemsetup -gettimezone
        try:
            out = subprocess.run(
                ['/usr/sbin/systemsetup', '-gettimezone'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=0.5,
            )
            if out.returncode == 0:
                line = out.stdout.strip()
                # Expected: "Time Zone: America/Los_Angeles"
                if ':' in line:
                    candidate = line.split(':', 1)[1].strip()
                    tz = SystemTimeDetector._extract_iana_from_any(candidate)
                    if tz:
                        return tz
        except Exception:
            pass

        # Read /etc/localtime like Unix
        return SystemTimeDetector._detect_timezone_unix()

    @staticmethod
    def _detect_timezone_windows() -> str | None:
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r'SYSTEM\CurrentControlSet\Control\TimeZoneInformation'
            ) as k:
                # "Time Zone Key Name" exists on newer Windows; fallback to "StandardName"
                try:
                    name, _ = winreg.QueryValueEx(k, 'Time Zone Key Name')
                    name = name.strip()
                except FileNotFoundError:
                    name, _ = winreg.QueryValueEx(k, 'StandardName')
                    name = name.strip()
                if name:
                    # Try mapping a few common Windows zones to IANA
                    mapped = SystemTimeDetector._win_to_iana_map().get(name)
                    if mapped:
                        return mapped
                    # If not mapped, return Windows name as last resort
                    return name
        except Exception:
            pass
        return None

    @staticmethod
    def _win_to_iana_map() -> dict:
        # Minimal mapping for common Windows time zones to IANA. Not exhaustive.
        return {
            'UTC': 'Etc/UTC',
            'GMT Standard Time': 'Europe/London',
            'W. Europe Standard Time': 'Europe/Berlin',
            'Central Europe Standard Time': 'Europe/Budapest',
            'Romance Standard Time': 'Europe/Paris',
            'Central European Standard Time': 'Europe/Warsaw',
            'E. Europe Standard Time': 'Europe/Bucharest',
            'Jordan Standard Time': 'Asia/Amman',
            'Egypt Standard Time': 'Africa/Cairo',
            'South Africa Standard Time': 'Africa/Johannesburg',
            'Russian Standard Time': 'Europe/Moscow',
            'Turkey Standard Time': 'Europe/Istanbul',
            'Israel Standard Time': 'Asia/Jerusalem',
            'Arab Standard Time': 'Asia/Riyadh',
            'Arabic Standard Time': 'Asia/Baghdad',
            'Iran Standard Time': 'Asia/Tehran',
            'Arabian Standard Time': 'Asia/Dubai',
            'Afghanistan Standard Time': 'Asia/Kabul',
            'Pakistan Standard Time': 'Asia/Karachi',
            'India Standard Time': 'Asia/Kolkata',
            'Bangladesh Standard Time': 'Asia/Dhaka',
            'SE Asia Standard Time': 'Asia/Bangkok',
            'China Standard Time': 'Asia/Shanghai',
            'Taipei Standard Time': 'Asia/Taipei',
            'Tokyo Standard Time': 'Asia/Tokyo',
            'Korea Standard Time': 'Asia/Seoul',
            'AUS Eastern Standard Time': 'Australia/Sydney',
            'E. Australia Standard Time': 'Australia/Brisbane',
            'Cen. Australia Standard Time': 'Australia/Adelaide',
            'AUS Central Standard Time': 'Australia/Darwin',
            'W. Australia Standard Time': 'Australia/Perth',
            'New Zealand Standard Time': 'Pacific/Auckland',
            'Tonga Standard Time': 'Pacific/Tongatapu',
            'Samoa Standard Time': 'Pacific/Apia',
            'Hawaiian Standard Time': 'Pacific/Honolulu',
            'Alaskan Standard Time': 'America/Anchorage',
            'Pacific Standard Time': 'America/Los_Angeles',
            'Pacific Standard Time (Mexico)': 'America/Tijuana',
            'US Mountain Standard Time': 'America/Phoenix',
            'Mountain Standard Time': 'America/Denver',
            'Mountain Standard Time (Mexico)': 'America/Chihuahua',
            'Central Standard Time': 'America/Chicago',
            'Central Standard Time (Mexico)': 'America/Mexico_City',
            'Canada Central Standard Time': 'America/Regina',
            'SA Pacific Standard Time': 'America/Bogota',
            'Eastern Standard Time': 'America/New_York',
            'SA Western Standard Time': 'America/La_Paz',
            'Atlantic Standard Time': 'America/Halifax',
            'Greenland Standard Time': 'America/Godthab',
            'Montevideo Standard Time': 'America/Montevideo',
            'Argentina Standard Time': 'America/Argentina/Buenos_Aires',
            'Bahia Standard Time': 'America/Bahia',
            'Magallanes Standard Time': 'America/Punta_Arenas',
            'Paraguay Standard Time': 'America/Asuncion',
            'SA Eastern Standard Time': 'America/Cayenne',
            'Azores Standard Time': 'Atlantic/Azores',
            'Cape Verde Standard Time': 'Atlantic/Cape_Verde',
            'Morocco Standard Time': 'Africa/Casablanca',
            'UTC-02': 'Etc/GMT+2',
            'UTC-11': 'Etc/GMT+11',
            'UTC-10': 'Etc/GMT+10',
            'UTC-09': 'Etc/GMT+9',
            'UTC-08': 'Etc/GMT+8',
            'UTC-07': 'Etc/GMT+7',
            'UTC-06': 'Etc/GMT+6',
            'UTC-05': 'Etc/GMT+5',
            'UTC-04': 'Etc/GMT+4',
            'UTC-03': 'Etc/GMT+3',
            'UTC-01': 'Etc/GMT+1',
            'UTC+01': 'Etc/GMT-1',
            'UTC+02': 'Etc/GMT-2',
            'UTC+03': 'Etc/GMT-3',
            'UTC+04': 'Etc/GMT-4',
            'UTC+05': 'Etc/GMT-5',
            'UTC+06': 'Etc/GMT-6',
            'UTC+07': 'Etc/GMT-7',
            'UTC+08': 'Etc/GMT-8',
            'UTC+09': 'Etc/GMT-9',
            'UTC+10': 'Etc/GMT-10',
            'UTC+11': 'Etc/GMT-11',
            'UTC+12': 'Etc/GMT-12',
        }
