
import locale
import time
from typing import Tuple


class SystemTimeDetector:
    @staticmethod
    def get_timezone() -> str:
        """
        Detect the system's current timezone name.

        Returns:
            str: The name of the current timezone. If daylight saving time is
                 in effect, the daylight timezone name is returned; otherwise
                 the standard timezone name is returned. If both names are
                 identical, that name is returned.
        """
        # time.tzname returns a tuple: (standard, daylight)
        tz_names: Tuple[str, str] = time.tzname
        # Determine if DST is currently in effect
        is_dst = time.daylight and time.localtime().tm_isdst > 0
        tz = tz_names[1] if is_dst else tz_names[0]
        # If both names are the same, just return one of them
        return tz if tz else tz_names[0]

    @staticmethod
    def get_time_format() -> str:
        """
        Detect whether the system uses a 12‑hour or 24‑hour time format.

        Returns:
            str: '12h' if the locale's time format includes an AM/PM marker,
                 otherwise '24h'.
        """
        try:
            # locale.nl_langinfo is available on POSIX systems
            time_format = locale.nl_langinfo(locale.T_FMT)
            # If the format string contains %p, it uses AM/PM
            if "%p" in time_format:
                return "12h"
        except Exception:
            # Fallback: try to infer from locale settings
            try:
                locale.setlocale(locale.LC_TIME, "")
                time_format = locale.nl_langinfo(locale.T_FMT)
                if "%p" in time_format:
                    return "12h"
            except Exception:
                pass

        # Default to 24‑hour format if detection fails
        return "24h"
