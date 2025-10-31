class SentinelHubRateLimit:
    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        if num_processes < 1:
            raise ValueError("num_processes must be >= 1")
        if minimum_wait_time < 0:
            raise ValueError("minimum_wait_time must be >= 0")
        if maximum_wait_time <= 0:
            raise ValueError("maximum_wait_time must be > 0")
        if minimum_wait_time > maximum_wait_time:
            raise ValueError(
                "minimum_wait_time cannot exceed maximum_wait_time")

        self.num_processes = int(num_processes)
        self.minimum_wait_time = float(minimum_wait_time)
        self.maximum_wait_time = float(maximum_wait_time)

        self._current_wait = self.minimum_wait_time
        self._initialized = False

    def register_next(self) -> float:
        return max(self.minimum_wait_time, min(self._current_wait, self.maximum_wait_time))

    def update(self, headers: dict, *, default: float) -> None:
        def _to_float(value):
            try:
                if value is None:
                    return None
                if isinstance(value, (int, float)):
                    return float(value)
                s = str(value).strip()
                if s == "":
                    return None
                return float(s)
            except Exception:
                return None

        def _parse_retry_after(hdrs):
            # Retry-After can be seconds or HTTP-date
            val = hdrs.get("retry-after")
            if val is None:
                return None
            # try seconds
            sec = _to_float(val)
            if sec is not None and sec >= 0:
                return sec
            # try HTTP-date
            try:
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(str(val))
                if dt is None:
                    return None
                import datetime as _dt
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=_dt.timezone.utc)
                now = _dt.datetime.now(_dt.timezone.utc)
                delta = (dt - now).total_seconds()
                return max(0.0, float(delta))
            except Exception:
                return None

        if not isinstance(headers, dict):
            headers = {}

        # normalize header keys
        lower_headers = {str(k).lower(): v for k, v in headers.items()}

        # Determine new base wait
        new_wait = None

        retry_after = _parse_retry_after(lower_headers)
        if retry_after is not None:
            # Respect server-mandated pause
            new_wait = max(float(default), float(retry_after))
        else:
            remaining = _to_float(
                lower_headers.get("x-ratelimit-remaining")
                or lower_headers.get("x-rate-limit-remaining")
                or lower_headers.get("x-rate-limit-remaining".replace("-", ""))
            )
            reset = _to_float(
                lower_headers.get("x-ratelimit-reset")
                or lower_headers.get("x-rate-limit-reset")
                or lower_headers.get("x-rate-limit-reset".replace("-", ""))
            )

            if reset is not None and reset < 0:
                reset = None

            if remaining is not None and reset is not None:
                if remaining <= 0:
                    candidate = max(reset, float(default))
                else:
                    # Average spacing to use full quota by reset
                    interval = reset / max(1.0, remaining)
                    # Scale for number of worker processes sharing the same account/quota
                    candidate = max(float(default), interval *
                                    float(self.num_processes))
                new_wait = candidate

        if new_wait is None:
            new_wait = float(default)

        # Clamp
        new_wait = max(self.minimum_wait_time, min(
            float(new_wait), self.maximum_wait_time))

        # Smooth updates to avoid jitter
        if not self._initialized:
            self._current_wait = new_wait
            self._initialized = True
        else:
            alpha = 0.3
            self._current_wait = alpha * new_wait + \
                (1.0 - alpha) * self._current_wait

        # Ensure bounds after smoothing
        self._current_wait = max(self.minimum_wait_time, min(
            self._current_wait, self.maximum_wait_time))
