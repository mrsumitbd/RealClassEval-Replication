import threading
import time
from email.utils import parsedate_to_datetime
from typing import Optional


class SentinelHubRateLimit:
    '''Class implementing rate limiting logic of Sentinel Hub service
    It has 2 public methods:
    - register_next - tells if next download can start or if not, what is the wait before it can be asked again
    - update - updates expectations according to headers obtained from download
    The rate limiting object is collecting information about the status of rate limiting policy buckets from
    Sentinel Hub service. According to this information and a feedback from download requests it adapts expectations
    about when the next download attempt will be possible.
    '''

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        '''
        :param num_processes: Number of parallel download processes running.
        :param minimum_wait_time: Minimum wait time between two consecutive download requests in seconds.
        :param maximum_wait_time: Maximum wait time between two consecutive download requests in seconds.
        '''
        if num_processes <= 0:
            raise ValueError("num_processes must be >= 1")
        if minimum_wait_time < 0:
            raise ValueError("minimum_wait_time must be >= 0")
        if maximum_wait_time <= 0:
            raise ValueError("maximum_wait_time must be > 0")
        if minimum_wait_time > maximum_wait_time:
            raise ValueError("minimum_wait_time must be <= maximum_wait_time")

        self._num_processes = int(num_processes)
        self._min_wait = float(minimum_wait_time)
        self._max_wait = float(maximum_wait_time)

        # Spread requests from multiple processes by splitting the minimum wait
        self._slot_interval = max(self._min_wait / self._num_processes, 0.0)

        self._lock = threading.Lock()
        self._next_mono = time.monotonic()

    def register_next(self) -> float:
        '''Determines if next download request can start or not by returning the waiting time in seconds.'''
        with self._lock:
            now = time.monotonic()
            wait = max(0.0, self._next_mono - now)
            if wait <= 0.0:
                # Reserve the next available slot immediately
                self._next_mono = max(
                    self._next_mono, now) + self._slot_interval
                return 0.0
            # Do not modify schedule if we are asked too early
            return min(wait, self._max_wait)

    def update(self, headers: dict, *, default: float) -> None:
        '''Update the next possible download time if the service has responded with the rate limit.
        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        '''
        headers = {str(k).lower(): str(v) for k, v in (headers or {}).items()}
        now_wall = time.time()
        now_mono = time.monotonic()

        wait_seconds = self._extract_wait_seconds(headers, now_wall)
        if wait_seconds is None:
            # Fallback to provided default (milliseconds)
            try:
                wait_seconds = max(0.0, float(default) / 1000.0)
            except Exception:
                wait_seconds = self._min_wait

        # Clamp to configured bounds
        wait_seconds = max(self._min_wait, min(wait_seconds, self._max_wait))

        with self._lock:
            target = now_mono + wait_seconds
            if target > self._next_mono:
                self._next_mono = target

    def _extract_wait_seconds(self, headers: dict, now_wall: float) -> Optional[float]:
        # Retry-After: either delta-seconds or HTTP-date
        ra = headers.get('retry-after')
        if ra:
            ra = ra.strip()
            # Try delta seconds
            try:
                val = float(ra)
                if val >= 0:
                    return val
            except ValueError:
                pass
            # Try HTTP-date
            dt = self._parse_http_date(ra)
            if dt is not None:
                ts = dt.timestamp()
                return max(0.0, ts - now_wall)

        # X-RateLimit-Reset-After: seconds to wait
        xr_after = headers.get(
            'x-ratelimit-reset-after') or headers.get('x-rate-limit-reset-after')
        if xr_after:
            try:
                val = float(xr_after)
                if val >= 0:
                    return val
            except ValueError:
                pass

        # X-RateLimit-Reset: absolute reset time (epoch seconds or milliseconds)
        xr = headers.get(
            'x-ratelimit-reset') or headers.get('x-rate-limit-reset')
        if xr:
            # Some services send epoch seconds; others epoch milliseconds.
            # Heuristic: > 1e11 ⇒ ms, > 1e10 sometimes ms; else seconds.
            try:
                reset_val = float(xr)
                if reset_val > 1e11:
                    reset_epoch = reset_val / 1000.0
                elif reset_val > 1e10:
                    reset_epoch = reset_val / 1000.0
                else:
                    reset_epoch = reset_val
                return max(0.0, reset_epoch - now_wall)
            except ValueError:
                # Sometimes they send HTTP-date here
                dt = self._parse_http_date(xr)
                if dt is not None:
                    return max(0.0, dt.timestamp() - now_wall)

        # Some providers specify window intervals; attempt conservative pacing
        # X-RateLimit-Interval: e.g., "1s", "10s", "1m"
        xint = headers.get(
            'x-ratelimit-interval') or headers.get('x-rate-limit-interval')
        if xint:
            secs = self._parse_duration_seconds(xint)
            if secs is not None and secs > 0:
                # Minimal wait is a fraction of interval considering processes
                return max(self._min_wait, secs / max(1, self._num_processes))

        return None

    @staticmethod
    def _parse_http_date(value: str):
        try:
            dt = parsedate_to_datetime(value)
            # Ensure timezone-aware datetime
            if dt is not None and dt.tzinfo is None:
                # Assume UTC if tz not provided
                from datetime import timezone
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None

    @staticmethod
    def _parse_duration_seconds(value: str) -> Optional[float]:
        s = value.strip().lower()
        try:
            # Plain number => seconds
            return float(s)
        except ValueError:
            pass
        # Support suffixes: ms, s, m, h
        units = [('ms', 1/1000.0), ('s', 1.0), ('m', 60.0), ('h', 3600.0)]
        for suf, mul in units:
            if s.endswith(suf):
                try:
                    return float(s[:-len(suf)].strip()) * mul
                except ValueError:
                    return None
        return None
