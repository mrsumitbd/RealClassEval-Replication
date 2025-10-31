
import time
from collections import deque
from typing import Deque


class RateLimiter:
    """
    A simple rate limiter that allows at most `max_calls` calls within a
    sliding window of `period` seconds. The `wait` method blocks until the
    next call is permitted.
    """

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        if max_calls <= 0:
            raise ValueError("max_calls must be a positive integer")
        if period <= 0:
            raise ValueError("period must be a positive number")

        self.max_calls: int = max_calls
        self.period: float = period
        self._timestamps: Deque[float] = deque()

    def wait(self):
        """
        Block until a new call is allowed under the rate limit.
        """
        now = time.monotonic()

        # Remove timestamps that are outside the sliding window
        while self._timestamps and now - self._timestamps[0] >= self.period:
            self._timestamps.popleft()

        if len(self._timestamps) < self.max_calls:
            # We can proceed immediately
            self._timestamps.append(now)
            return

        # Need to wait until the oldest timestamp is outside the window
        oldest = self._timestamps[0]
        sleep_time = self.period - (now - oldest)
        if sleep_time > 0:
            time.sleep(sleep_time)

        # After sleeping, purge old timestamps again
        now = time.monotonic()
        while self._timestamps and now - self._timestamps[0] >= self.period:
            self._timestamps.popleft()

        self._timestamps.append(now)
