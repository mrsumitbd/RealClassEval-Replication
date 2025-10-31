from typing import Any, Dict, List, Optional, Set, Union
import platform
import locale
import subprocess

class TimeFormatDetector:
    """Unified time format detection using multiple strategies."""
    TWELVE_HOUR_COUNTRIES: Set[str] = {'US', 'CA', 'AU', 'NZ', 'PH', 'IN', 'EG', 'SA', 'CO', 'PK', 'MY', 'GH', 'KE', 'NG', 'PE', 'ZA', 'LK', 'BD', 'JO', 'SG', 'IE', 'MT', 'GB'}

    @classmethod
    def detect_from_cli(cls, args: Any) -> Optional[bool]:
        """Detect from CLI arguments.

        Returns:
            True for 12h format, False for 24h, None if not specified
        """
        if args and hasattr(args, 'time_format'):
            if args.time_format == '12h':
                return True
            if args.time_format == '24h':
                return False
        return None

    @classmethod
    def detect_from_timezone(cls, timezone_name: str) -> Optional[bool]:
        """Detect using Babel/timezone data.

        Returns:
            True for 12h format, False for 24h, None if cannot determine
        """
        if not HAS_BABEL:
            return None
        try:
            location: Optional[str] = get_timezone_location(timezone_name, locale_name='en_US')
            if location:
                for country_code in cls.TWELVE_HOUR_COUNTRIES:
                    if country_code in location or location.endswith(country_code):
                        return True
            return False
        except Exception:
            return None

    @classmethod
    def detect_from_locale(cls) -> bool:
        """Detect from system locale.

        Returns:
            True for 12h format, False for 24h
        """
        try:
            locale.setlocale(locale.LC_TIME, '')
            time_str: str = locale.nl_langinfo(locale.T_FMT_AMPM)
            if time_str:
                return True
            dt_fmt: str = locale.nl_langinfo(locale.D_T_FMT)
            return bool('%p' in dt_fmt or '%I' in dt_fmt)
        except Exception:
            return False

    @classmethod
    def detect_from_system(cls) -> str:
        """Platform-specific system detection.

        Returns:
            '12h' or '24h'
        """
        system: str = platform.system()
        if system == 'Darwin':
            try:
                result: subprocess.CompletedProcess[str] = subprocess.run(['defaults', 'read', 'NSGlobalDomain', 'AppleICUForce12HourTime'], capture_output=True, text=True, check=False)
                if result.returncode == 0 and result.stdout.strip() == '1':
                    return '12h'
                date_result: subprocess.CompletedProcess[str] = subprocess.run(['date', '+%r'], capture_output=True, text=True, check=True)
                date_output: str = date_result.stdout.strip()
                if 'AM' in date_output or 'PM' in date_output:
                    return '12h'
            except Exception:
                pass
        elif system == 'Linux':
            try:
                locale_result: subprocess.CompletedProcess[str] = subprocess.run(['locale', 'LC_TIME'], capture_output=True, text=True, check=True)
                lc_time: str = locale_result.stdout.strip().split('=')[-1].strip('"')
                if lc_time and any((x in lc_time for x in ['en_US', 'en_CA', 'en_AU'])):
                    return '12h'
            except Exception:
                pass
        elif system == 'Windows':
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\International') as key:
                    time_fmt: str = winreg.QueryValueEx(key, 'sTimeFormat')[0]
                    if 'h' in time_fmt and ('tt' in time_fmt or 't' in time_fmt):
                        return '12h'
            except Exception:
                pass
        return '12h' if cls.detect_from_locale() else '24h'

    @classmethod
    def get_preference(cls, args: Any=None, timezone_name: Optional[str]=None) -> bool:
        """Main entry point - returns True for 12h, False for 24h."""
        cli_pref: Optional[bool] = cls.detect_from_cli(args)
        if cli_pref is not None:
            return cli_pref
        if timezone_name:
            tz_pref: Optional[bool] = cls.detect_from_timezone(timezone_name)
            if tz_pref is not None:
                return tz_pref
        return cls.detect_from_system() == '12h'