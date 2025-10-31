
import locale
import time
from typing import Optional

try:
    # tzlocal is a small dependency that works on most platforms
    from tzlocal import get_localzone_name
except Exception:  # pragma: no cover
    get_localzone_name = None  # type: ignore


class SystemTimeDetector:
    """System timezone and time format detection."""

    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone.

        Returns:
            The name of the local timezone (e.g. ``'America/New_York'``).
            If the timezone cannot be determined, ``'UTC'`` is returned.
        """
        # Prefer tzlocal if available
        if get_localzone_name is not None:
            try:
                tz = get_localzone_name()
                if tz:
                    return tz
            except Exception:  # pragma: no cover
                pass

        # Fallback to the POSIX TZ environment variable
        tz_env = time.tzname[0]
        if tz_env and tz_env != 'UTC':
            return tz_env

        # Final fallback
        return 'UTC'

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h').

        The detection is based on the locale's time format string.  If the
        locale's ``T_FMT`` contains ``%p`` (AM/PM), a 12‑hour clock is
        assumed; otherwise a 24‑hour clock is assumed.

        Returns:
            ``'12h'`` or ``'24h'``.
        """
        # Try to use the locale's time format string
        try:
            fmt = locale.nl_langinfo(locale.T_FMT)
            if '%p' in fmt:
                return '12h'
        except Exception:  # pragma: no cover
            pass

        # Fallback: check what time.strftime('%p') returns
        am_pm = time.strftime('%p')
        if am_pm in ('AM', 'PM'):
            return '12h'

        return '24h'
