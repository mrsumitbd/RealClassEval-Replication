class SystemTimeDetector:

    @staticmethod
    def get_timezone() -> str:
        from datetime import datetime
        import time as _time

        try:
            local_dt = datetime.now().astimezone()
            name = local_dt.tzname()
            if name:
                return name
        except Exception:
            pass

        try:
            is_dst = _time.localtime().tm_isdst > 0
            if _time.daylight and is_dst:
                return _time.tzname[1] or "Local"
            return _time.tzname[0] or "Local"
        except Exception:
            return "Local"

    @staticmethod
    def get_time_format() -> str:
        import time
        import locale

        # Try POSIX nl_langinfo if available
        try:
            if hasattr(locale, "nl_langinfo") and hasattr(locale, "T_FMT"):
                # type: ignore[attr-defined]
                fmt = locale.nl_langinfo(locale.T_FMT)
                if ("%I" in fmt) or ("%p" in fmt):
                    return "12-hour"
                return "24-hour"
        except Exception:
            pass

        # Fallback: check if AM/PM marker appears
        try:
            if time.strftime("%p"):
                return "12-hour"
            sample = time.strftime("%X")
            if any(marker in sample.upper() for marker in ("AM", "PM")):
                return "12-hour"
        except Exception:
            pass

        return "24-hour"
