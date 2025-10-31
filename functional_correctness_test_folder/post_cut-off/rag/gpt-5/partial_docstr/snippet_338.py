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
        if not isinstance(max_calls, int) or max_calls < 1:
            raise ValueError("max_calls must be a positive integer")
        if not isinstance(period, (int, float)) or period <= 0:
            raise ValueError("period must be a positive number")
        self.max_calls = max_calls
        self.period = float(period)
        self._timestamps = deque()
        self._lock = threading.Lock()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        while True:
            now = time.monotonic()
            with self._lock:
                cutoff = now - self.period
                while self._timestamps and self._timestamps[0] <= cutoff:
                    self._timestamps.popleft()

                if len(self._timestamps) < self.max_calls:
                    self._timestamps.append(now)
                    return

                sleep_time = max(
                    0.0, (self._timestamps[0] + self.period) - now)

            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Yield to avoid tight loop in edge timing cases
                time.sleep(0)
