import time
import threading
from collections import deque


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
            raise ValueError("max_calls must be > 0")
        if period <= 0:
            raise ValueError("period must be > 0")
        self.max_calls = int(max_calls)
        self.period = float(period)
        self._calls = deque()
        self._cond = threading.Condition()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self._cond:
            now = time.monotonic()
            while True:
                # Purge timestamps outside the window
                while self._calls and (now - self._calls[0]) >= self.period:
                    self._calls.popleft()

                if len(self._calls) < self.max_calls:
                    self._calls.append(now)
                    self._cond.notify_all()
                    return

                earliest = self._calls[0]
                sleep_time = self.period - (now - earliest)
                if sleep_time <= 0:
                    now = time.monotonic()
                    continue
                self._cond.wait(timeout=sleep_time)
                now = time.monotonic()
