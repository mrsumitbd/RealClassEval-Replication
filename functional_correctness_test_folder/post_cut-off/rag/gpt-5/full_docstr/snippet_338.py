import threading
import time
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
        if max_calls < 1:
            raise ValueError("max_calls must be >= 1")
        if period <= 0:
            raise ValueError("period must be > 0")

        self.max_calls = int(max_calls)
        self.period = float(period)
        self._timestamps = deque()
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self._cond:
            while True:
                now = time.monotonic()
                while self._timestamps and (now - self._timestamps[0]) >= self.period:
                    self._timestamps.popleft()

                if len(self._timestamps) < self.max_calls:
                    self._timestamps.append(now)
                    return

                earliest = self._timestamps[0]
                delay = self.period - (now - earliest)
                if delay > 0:
                    self._cond.wait(delay)
