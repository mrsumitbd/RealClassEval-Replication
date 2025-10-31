
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
            The IANA timezone name (e.g. ``America/New_York``) if available,
            otherwise the local timezone abbreviation from :mod:`time`.
        """
        if get_localzone_name is not None:
            try:
                return get_localzone_name()
            except Exception:  # pragma: no cover
                pass
        # Fallback: use the first element of time.tzname
        return time.tzname[0] or "UTC"

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format.

        Returns:
            ``'12h'`` if the locale uses AM/PM notation, otherwise ``'24h'``.
        """
        # ``%p`` returns AM/PM if the locale uses 12‑hour format.
        am_pm = time.strftime("%p")
        if am_pm and am_pm.upper() in ("AM", "PM"):
            return "12h"

        # Some locales may use a different AM/PM string; check the locale
        # specific AM/PM strings if available.
        try:
            am_pm_locale = locale.nl_langinfo(locale.AM_STR)
            pm_pm_locale = locale.nl_langinfo(locale.PM_STR)
            if am_pm_locale or pm_pm_locale:
                return "12h"
        except Exception:  # pragma: no cover
            pass

        return "24h"
