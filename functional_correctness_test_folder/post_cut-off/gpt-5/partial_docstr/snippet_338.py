import time
import threading
from collections import deque


class RateLimiter:

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
        self._calls = deque()
        self._lock = threading.Lock()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        while True:
            with self._lock:
                now = time.monotonic()
                # Remove calls outside the current window
                while self._calls and (now - self._calls[0]) >= self.period:
                    self._calls.popleft()

                if len(self._calls) < self.max_calls:
                    self._calls.append(now)
                    return

                oldest = self._calls[0]
                sleep_for = self.period - (now - oldest)

            if sleep_for > 0:
                time.sleep(sleep_for)
            else:
                # In case of timing edge cases, loop without sleeping
                continue
