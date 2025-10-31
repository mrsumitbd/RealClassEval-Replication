import threading
import time
from typing import Optional, Dict, Any


class SentinelHubRateLimit:

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
            raise ValueError(
                "minimum_wait_time cannot be greater than maximum_wait_time")

        self._num_processes = int(num_processes)
        self._min_wait = float(minimum_wait_time)
        self._max_wait = float(maximum_wait_time)

        self._lock = threading.Lock()
        self._next_time_monotonic = 0.0

    def register_next(self) -> float:
        now = time.monotonic()
        with self._lock:
            wait = max(0.0, self._next_time_monotonic - now)
            # Enforce minimum spacing between consecutive requests globally.
            step = self._min_wait
            self._next_time_monotonic = max(
                self._next_time_monotonic, now) + step
        return wait

    def update(self, headers: Dict[str, Any], *, default: float) -> None:
        '''Update the next possible download time if the service has responded with the rate limit.
        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        '''
        if headers is None:
            headers = {}
        lower = {str(k).lower(): v for k, v in headers.items()}
        wait_seconds: Optional[float] = None

        # 1) Retry-After header (seconds or HTTP-date). We handle numeric only.
        ra = lower.get('retry-after')
        if ra is not None:
            try:
                wait_seconds = float(ra)
            except (TypeError, ValueError):
                wait_seconds = None

        # 2) Millisecond-based retry headers
        if wait_seconds is None:
            ra_ms = lower.get(
                'retry-after-ms') or lower.get('x-retry-after-ms')
            if ra_ms is not None:
                try:
                    wait_seconds = float(ra_ms) / 1000.0
                except (TypeError, ValueError):
                    wait_seconds = None

        # 3) Rate limit reset semantics
        if wait_seconds is None:
            remaining = lower.get(
                'x-ratelimit-remaining') or lower.get('ratelimit-remaining')
            reset = lower.get(
                'x-ratelimit-reset') or lower.get('ratelimit-reset')
            if reset is not None:
                now_wall = time.time()
                # Try to parse remaining
                rem_val: Optional[int] = None
                try:
                    rem_val = int(
                        str(remaining)) if remaining is not None else None
                except (TypeError, ValueError):
                    rem_val = None

                # Parse reset: could be epoch seconds, epoch ms, or delta seconds
                reset_val: Optional[float] = None
                try:
                    r = float(str(reset))
                    # Heuristics for units
                    if r > 1e12:   # microseconds epoch
                        reset_val = r / 1e6
                    elif r > 1e11:  # milliseconds epoch
                        reset_val = r / 1e3
                    elif r > 1e9:  # seconds epoch
                        reset_val = r
                    else:
                        # Treat as delta seconds
                        wait_seconds = r
                except (TypeError, ValueError):
                    reset_val = None

                if wait_seconds is None and reset_val is not None:
                    # We have an absolute reset time
                    delta = max(0.0, reset_val - now_wall)
                    # Only apply if we are out of quota or delta is meaningful
                    if rem_val is None or rem_val <= 0 or delta > 0:
                        wait_seconds = delta

        # 4) Default if still unknown (default is provided in milliseconds)
        if wait_seconds is None:
            try:
                wait_seconds = float(default) / 1000.0
            except (TypeError, ValueError):
                wait_seconds = self._min_wait

        # Clamp to configured bounds
        if self._max_wait is not None:
            wait_seconds = min(wait_seconds, self._max_wait)
        wait_seconds = max(wait_seconds, self._min_wait)

        target = time.monotonic() + wait_seconds
        with self._lock:
            if target > self._next_time_monotonic:
                self._next_time_monotonic = target
