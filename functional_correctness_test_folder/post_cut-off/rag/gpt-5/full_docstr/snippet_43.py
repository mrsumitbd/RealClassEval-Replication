import os
import sys
import time
import locale
import platform
import pathlib
import subprocess
import datetime


class SystemTimeDetector:
    """System timezone and time format detection."""

    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        # 1) Try environment variable
        tz_env = os.environ.get('TZ')
        if tz_env:
            tz_env = tz_env.strip()
            if tz_env:
                return tz_env

        # 2) Try tzlocal if available
        try:
            import tzlocal  # type: ignore
            try:
                # tzlocal >= 3
                name = tzlocal.get_localzone_name()
            except Exception:
                # tzlocal < 3
                name = str(tzlocal.get_localzone())
            if name:
                return name
        except Exception:
            pass

        # 3) Platform-specific methods
        if os.name == 'nt':
            # Windows registry
            try:
                import winreg  # type: ignore

                def _read_reg(root, path, name):
                    try:
                        with winreg.OpenKey(root, path) as k:
                            val, _ = winreg.QueryValueEx(k, name)
                            return val
                    except Exception:
                        return None

                # Prefer the key name if available
                key_path = r'SYSTEM\CurrentControlSet\Control\TimeZoneInformation'
                name = _read_reg(winreg.HKEY_LOCAL_MACHINE,
                                 key_path, 'TimeZoneKeyName')
                if not name:
                    name = _read_reg(winreg.HKEY_LOCAL_MACHINE,
                                     key_path, 'Time Zone Key Name')
                if not name:
                    # Fallback to StandardName (localized)
                    name = _read_reg(winreg.HKEY_LOCAL_MACHINE,
                                     key_path, 'StandardName')
                if name:
                    return str(name)
            except Exception:
                pass
        else:
            # systemd-based Linux
            def _run_cmd(args):
                try:
                    out = subprocess.check_output(
                        args, stderr=subprocess.DEVNULL)
                    return out.decode(errors='ignore').strip()
                except Exception:
                    return None

            out = _run_cmd(
                ['timedatectl', 'show', '-p', 'Timezone', '--value'])
            if out:
                return out

            # Older timedatectl output
            out = _run_cmd(['timedatectl'])
            if out:
                for line in out.splitlines():
                    if 'Time zone:' in line:
                        # Example: "Time zone: Europe/Berlin (CEST, +0200)"
                        part = line.split(':', 1)[1].strip()
                        zone = part.split(' ', 1)[0].strip()
                        if zone:
                            return zone

            # macOS
            if sys.platform == 'darwin':
                out = _run_cmd(['systemsetup', '-gettimezone'])
                if out and 'Time Zone:' in out:
                    zone = out.split(':', 1)[1].strip()
                    if zone:
                        return zone

            # Debian/Ubuntu-like
            try:
                tzfile = pathlib.Path('/etc/timezone')
                if tzfile.exists():
                    content = tzfile.read_text(
                        encoding='utf-8', errors='ignore').strip()
                    if content:
                        return content
            except Exception:
                pass

            # Generic Unix: parse /etc/localtime symlink/realpath
            try:
                p = pathlib.Path('/etc/localtime')
                if p.exists():
                    rp = os.path.realpath(str(p))
                    for marker in ('/zoneinfo/', 'zoneinfo/'):
                        idx = rp.find(marker)
                        if idx != -1:
                            zone = rp[idx + len(marker):].strip(os.sep)
                            if zone:
                                return zone
            except Exception:
                pass

        # 4) Fallback to tzinfo name
        try:
            tzinfo = datetime.datetime.now(
                datetime.timezone.utc).astimezone().tzinfo
            if tzinfo:
                # zoneinfo.ZoneInfo has .key
                name = getattr(tzinfo, 'key', None)
                if not name:
                    name = tzinfo.tzname(None)
                if name:
                    return str(name)
        except Exception:
            pass

        # 5) Final fallback
        try:
            if time.tzname and time.tzname[0]:
                return time.tzname[0]
        except Exception:
            pass
        return 'UTC'

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        # Helper to run external commands
        def _run_cmd(args):
            try:
                out = subprocess.check_output(args, stderr=subprocess.DEVNULL)
                return out.decode(errors='ignore').strip()
            except Exception:
                return None

        # Windows: check registry in current user profile
        if os.name == 'nt':
            try:
                import winreg  # type: ignore

                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Control Panel\International') as k:
                    try:
                        v, _ = winreg.QueryValueEx(k, 'iTime')
                        if str(v) == '1':
                            return '24h'
                        if str(v) == '0':
                            return '12h'
                    except Exception:
                        pass
                    # Inspect time format strings if present
                    for reg_name in ('sShortTime', 'sTimeFormat'):
                        try:
                            fmt, _ = winreg.QueryValueEx(k, reg_name)
                            if isinstance(fmt, str) and fmt:
                                if 'H' in fmt:
                                    return '24h'
                                if 'h' in fmt and 'H' not in fmt:
                                    return '12h'
                        except Exception:
                            pass
            except Exception:
                pass

        # macOS: user defaults
        if sys.platform == 'darwin':
            out = _run_cmd(['defaults', 'read', '-g',
                           'AppleICUForce24HourTime'])
            if out:
                v = out.strip().lower()
                if v in ('1', 'yes', 'true'):
                    return '24h'
                if v in ('0', 'no', 'false'):
                    return '12h'
            # Fallback: inspect time format strings if available
            out = _run_cmd(['defaults', 'read', '-g',
                           'AppleICUTimeFormatStrings'])
            if out:
                if 'H' in out:
                    return '24h'
                if 'h' in out and 'H' not in out:
                    return '12h'

        # GNOME (Linux)
        out = _run_cmd(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'clock-format'])
        if out:
            if '24h' in out:
                return '24h'
            if '12h' in out:
                return '12h'

        # Locale-based inference (POSIX, generic fallback)
        try:
            fmt = None
            if hasattr(locale, 'nl_langinfo'):
                try:
                    fmt = locale.nl_langinfo(locale.T_FMT)
                except Exception:
                    fmt = None

            if fmt:
                # Format a known 13:00 time to detect hour cycle
                tt = time.struct_time((2000, 1, 1, 13, 0, 0, 5, 1, -1))
                try:
                    rendered = time.strftime(fmt, tt)
                    if '13' in rendered:
                        return '24h'
                    # If directives are present, infer from them
                    if '%H' in fmt:
                        return '24h'
                    if '%I' in fmt or '%p' in fmt or '%r' in fmt:
                        return '12h'
                except Exception:
                    pass

            # Fallback to %X with synthetic 13:00
            tt = time.struct_time((2000, 1, 1, 13, 0, 0, 5, 1, -1))
            rendered = time.strftime('%X', tt)
            if '13' in rendered:
                return '24h'
            # Heuristic for AM/PM markers
            low = rendered.lower()
            if 'am' in low or 'pm' in low:
                return '12h'
        except Exception:
            pass

        # Final default
        return '24h'
