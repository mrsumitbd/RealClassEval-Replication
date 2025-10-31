
import locale
import time
from typing import Optional

try:
    # tzlocal is a small dependency that provides the full IANA timezone name
    from tzlocal import get_localzone_name
except Exception:  # pragma: no cover
    get_localzone_name = None  # type: ignore


class SystemTimeDetector:
    """System timezone and time format detection."""

    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone.

        Returns:
            The IANA timezone name if available, otherwise the local
            abbreviation from :mod:`time`.
        """
        if get_localzone_name is not None:
            try:
                tz = get_localzone_name()
                if tz:
                    return tz
            except Exception:  # pragma: no cover
                pass

        # Fallback to the abbreviation from the C library
        return time.tzname[0] or "UTC"

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h').

        The detection is based on the presence of AM/PM markers in the
        locale's time format. If the locale does not provide AM/PM
        markers, a 24‑hour format is assumed.

        Returns:
            '12h' or '24h'
        """
        # Try locale's AM/PM format string
        try:
            ampm = locale.nl_langinfo(locale.T_FMT_AMPM)
            if ampm:
                return "12h"
        except Exception:  # pragma: no cover
            pass

        # Fallback: check the result of strftime('%p')
        ampm = time.strftime("%p")
        if ampm and ampm.upper() in ("AM", "PM"):
            return "12h"

        return "24h"
