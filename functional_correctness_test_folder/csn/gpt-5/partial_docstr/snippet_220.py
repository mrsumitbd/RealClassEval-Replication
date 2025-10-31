class RateLimitsInfo:
    def __init__(self, limit=None, remaining=None, reset_at=None, retry_after=None, source=None):
        self.limit = limit
        self.remaining = remaining
        self.reset_at = reset_at  # aware datetime in UTC or None
        self.retry_after = retry_after  # seconds or None
        # where it was parsed from (e.g., 'headers' or 'dict')
        self.source = source

    def __str__(self):
        parts = []
        if self.limit is not None:
            parts.append(f"limit={self.limit}")
        if self.remaining is not None:
            parts.append(f"remaining={self.remaining}")
        if self.reset_at is not None:
            parts.append(f"reset_at={self.reset_at.isoformat()}")
        if self.retry_after is not None:
            parts.append(f"retry_after={self.retry_after}s")
        if not parts:
            return "RateLimitsInfo()"
        return "RateLimitsInfo(" + ", ".join(parts) + ")"

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        if data is None:
            return cls(source="dict")
        # Normalize keys (case-insensitive, underscores and hyphens treated similarly)
        norm = {}
        for k, v in data.items():
            if not isinstance(k, str):
                continue
            key = k.strip().lower().replace("-", "_")
            norm[key] = v

        limit = cls._to_int(norm.get("limit", norm.get("ratelimit_limit")))
        remaining = cls._to_int(
            norm.get("remaining", norm.get("ratelimit_remaining")))
        retry_after = cls._to_int(norm.get("retry_after"))

        reset_at = None
        # Accept 'reset_at' as ISO or datetime, 'reset' as seconds delta, 'reset_epoch' as unix ts
        reset_iso = norm.get("reset_at") or norm.get("reset_time")
        reset_epoch = norm.get("reset_epoch") or norm.get(
            "epoch") or norm.get("ratelimit_reset_epoch")
        reset_generic = norm.get("reset") or norm.get("ratelimit_reset")

        reset_at = cls._parse_reset_any(reset_iso, reset_epoch, reset_generic)

        return cls(limit=limit, remaining=remaining, reset_at=reset_at, retry_after=retry_after, source="dict")

    @classmethod
    def from_headers(cls, headers):
        if headers is None:
            return cls(source="headers")
        # headers may be a mapping with case-insensitive keys; normalize to lowercase

        def get_header(*names):
            for name in names:
                for k, v in headers.items():
                    if isinstance(k, str) and k.lower() == name.lower():
                        return v
            return None

        limit = cls._to_int(
            get_header("x-ratelimit-limit", "ratelimit-limit")
        )
        remaining = cls._to_int(
            get_header("x-ratelimit-remaining", "ratelimit-remaining")
        )

        # Reset can be:
        # - X-RateLimit-Reset: unix epoch seconds (GitHub, Twitter) OR delta seconds (some APIs)
        # - RateLimit-Reset: delta seconds per RFC (can be seconds or a timestamp)
        # - Retry-After: delta seconds (or HTTP-date)
        h_reset = get_header("x-ratelimit-reset", "ratelimit-reset")
        retry_after_raw = get_header("retry-after")

        reset_at = cls._parse_reset_any(
            None, h_reset, h_reset)  # parse both interpretations
        retry_after = cls._parse_retry_after(retry_after_raw)

        # If we only have Retry-After and no reset_at, derive reset_at as now + retry_after
        if reset_at is None and retry_after is not None:
            reset_at = cls._now_utc() + cls._seconds_to_timedelta(retry_after)

        return cls(limit=limit, remaining=remaining, reset_at=reset_at, retry_after=retry_after, source="headers")

    @staticmethod
    def _to_int(value):
        if value is None:
            return None
        try:
            return int(float(str(value).strip()))
        except Exception:
            return None

    @staticmethod
    def _now_utc():
        from datetime import datetime, timezone
        return datetime.now(timezone.utc)

    @staticmethod
    def _seconds_to_timedelta(seconds):
        from datetime import timedelta
        try:
            s = int(float(seconds))
            return timedelta(seconds=s)
        except Exception:
            return timedelta(0)

    @classmethod
    def _parse_reset_any(cls, reset_iso, reset_epoch_or_delta, reset_delta=None):
        # Try ISO datetime first
        dt = cls._parse_iso_datetime(reset_iso)
        if dt is not None:
            return dt

        # Try epoch seconds
        dt = cls._parse_epoch_or_delta(reset_epoch_or_delta)
        if dt is not None:
            return dt

        # Fallback: explicit delta seconds
        dt = cls._parse_delta_seconds(reset_delta)
        if dt is not None:
            return dt
        return None

    @classmethod
    def _parse_iso_datetime(cls, value):
        if not value:
            return None
        from datetime import datetime, timezone
        s = str(value).strip()
        # Accept RFC1123/HTTP-date for Retry-After too
        for fmt in (
            "%a, %d %b %Y %H:%M:%S GMT",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ):
            try:
                parsed = datetime.strptime(s, fmt)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                else:
                    parsed = parsed.astimezone(timezone.utc)
                return parsed
            except Exception:
                continue
        # Try fromisoformat
        try:
            parsed = datetime.fromisoformat(s)
            if parsed.tzinfo is None:
                from datetime import timezone
                parsed = parsed.replace(tzinfo=timezone.utc)
            else:
                parsed = parsed.astimezone(timezone.utc)
            return parsed
        except Exception:
            return None

    @classmethod
    def _parse_epoch_or_delta(cls, value):
        if value is None:
            return None
        s = str(value).strip()
        # If it's clearly not numeric, skip
        try:
            num = float(s)
        except Exception:
            return None

        # Heuristic:
        # - If value > 10^7, treat as Unix epoch seconds (e.g., 1739021123)
        # - Else, treat as delta seconds from now
        # Also accept milliseconds if > 10^12
        from datetime import datetime, timezone, timedelta
        now = cls._now_utc()
        if num > 1e12:  # milliseconds epoch
            seconds = num / 1000.0
            try:
                return datetime.fromtimestamp(seconds, tz=timezone.utc)
            except Exception:
                return None
        if num > 1e7:  # epoch seconds
            try:
                return datetime.fromtimestamp(num, tz=timezone.utc)
            except Exception:
                return None
        # treat as delta seconds
        try:
            return now + timedelta(seconds=int(num))
        except Exception:
            return None

    @classmethod
    def _parse_delta_seconds(cls, value):
        if value is None:
            return None
        try:
            sec = int(float(str(value).strip()))
        except Exception:
            return None
        return cls._now_utc() + cls._seconds_to_timedelta(sec)

    @classmethod
    def _parse_retry_after(cls, value):
        if value is None:
            return None
        s = str(value).strip()
        # Retry-After can be delta seconds or HTTP-date
        # Try seconds first
        try:
            return int(float(s))
        except Exception:
            pass
        # Try HTTP-date
        dt = cls._parse_iso_datetime(s)
        if dt is None:
            return None
        delta = dt - cls._now_utc()
        seconds = int(max(0, round(delta.total_seconds())))
        return seconds
