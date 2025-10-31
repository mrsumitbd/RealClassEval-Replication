from collections import deque
import threading
import time
from typing import Deque


class RateLimiter:
    '''Simple rate limiter to ensure we don't exceed API rate limits.'''

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        '''
        Initialize the rate limiter.
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        '''
        if max_calls <= 0:
            raise ValueError("max_calls must be a positive integer")
        if period <= 0:
            raise ValueError("period must be a positive number")

        self.max_calls = int(max_calls)
        self.period = float(period)
        self._calls: Deque[float] = deque()
        self._lock = threading.Lock()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        while True:
            with self._lock:
                now = time.monotonic()
                # Remove timestamps outside the period window
                cutoff = now - self.period
                while self._calls and self._calls[0] <= cutoff:
                    self._calls.popleft()

                if len(self._calls) < self.max_calls:
                    self._calls.append(now)
                    return

                sleep_time = self._calls[0] + self.period - now

            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # In case of clock drift or edge rounding, yield briefly
                time.sleep(0)
