from datetime import datetime, timezone
from typing import Optional, Union, Any


class TimestampProcessor:
    def __init__(self, timezone_handler: Optional[Any] = None) -> None:
        self._tz_handler = timezone_handler

    def parse_timestamp(self, timestamp_value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
        if timestamp_value is None:
            return None

        dt: Optional[datetime] = None

        if isinstance(timestamp_value, datetime):
            dt = timestamp_value

        elif isinstance(timestamp_value, (int, float)):
            dt = self._from_unix(timestamp_value)

        elif isinstance(timestamp_value, str):
            dt = self._from_string(timestamp_value.strip())

        if dt is None:
            return None

        dt = self._normalize_datetime(dt)
        dt = self._apply_timezone_handler(dt)
        return dt

    def _from_unix(self, value: Union[int, float]) -> datetime:
        val = float(value)

        abs_val = abs(val)
        # Heuristics for seconds/milliseconds/microseconds
        # - seconds typical: ~1e9 to 2e9 (for current dates)
        # - milliseconds: ~1e12 to 2e12
        # - microseconds: ~1e15 to 2e15
        if abs_val >= 1e14:
            seconds = val / 1_000_000.0
        elif abs_val >= 1e11:
            seconds = val / 1_000.0
        else:
            seconds = val

        try:
            return datetime.fromtimestamp(seconds, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            # Fallback: try as naive UTC if system cannot handle range
            epoch = datetime(1970, 1, 1)
            return epoch + timedelta(seconds=seconds)

    def _from_string(self, s: str) -> Optional[datetime]:
        if not s:
            return None

        # Handle Zulu suffix
        if s.endswith("Z") or s.endswith("z"):
            try:
                return datetime.fromisoformat(s[:-1]).replace(tzinfo=timezone.utc)
            except ValueError:
                pass

        # Try Python's ISO parser
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            pass

        # Common fallback formats
        fmts = [
            "%Y-%m-%d %H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y/%m/%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d",
            "%Y-%m-%d",
        ]
        for fmt in fmts:
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue

        # Try to parse fractional seconds without timezone if T present
        if "T" in s:
            parts = s.split("T", 1)
            if len(parts) == 2 and "." in parts[1]:
                try:
                    base, frac = parts[1].split(".", 1)
                    frac = "".join(ch for ch in frac if ch.isdigit())[:6]
                    candidate = f"{parts[0]} {base}.{frac}"
                    return datetime.strptime(candidate, "%Y-%m-%d %H:%M:%S.%f")
                except Exception:
                    pass

        return None

    def _normalize_datetime(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            # Assume UTC for naive datetimes by default
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def _apply_timezone_handler(self, dt: datetime) -> datetime:
        handler = self._tz_handler
        if handler is None:
            return dt

        # Try common method names to let a provided handler adjust the timezone
        for attr in ("ensure_timezone", "localize_naive", "localize", "attach_timezone"):
            func = getattr(handler, attr, None)
            if callable(func):
                try:
                    dt = func(dt)
                    break
                except Exception:
                    pass

        for attr in ("to_utc", "convert_to_utc", "normalize", "convert"):
            func = getattr(handler, attr, None)
            if callable(func):
                try:
                    out = func(dt)
                    if isinstance(out, datetime):
                        dt = out
                    break
                except Exception:
                    pass

        return dt
