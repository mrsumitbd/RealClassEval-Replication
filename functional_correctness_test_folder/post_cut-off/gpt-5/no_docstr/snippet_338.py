from collections import deque
from threading import Lock
from time import monotonic, sleep
from typing import Deque


class RateLimiter:
    def __init__(self, max_calls: int = 3, period: float = 1.0):
        if max_calls < 1:
            raise ValueError("max_calls must be >= 1")
        if period < 0:
            raise ValueError("period must be >= 0")
        self.max_calls: int = max_calls
        self.period: float = period
        self._calls: Deque[float] = deque()
        self._lock = Lock()

    def wait(self):
        if self.period == 0:
            # All calls allowed immediately when period is zero
            return

        while True:
            with self._lock:
                now = monotonic()
                # Remove expired calls
                while self._calls and (now - self._calls[0]) >= self.period:
                    self._calls.popleft()

                if len(self._calls) < self.max_calls:
                    self._calls.append(now)
                    return

                # Need to wait until the earliest call expires
                oldest = self._calls[0]
                sleep_time = self.period - (now - oldest)

            if sleep_time > 0:
                sleep(sleep_time)
            else:
                # If computed non-positive, loop will clean up and proceed
                pass
