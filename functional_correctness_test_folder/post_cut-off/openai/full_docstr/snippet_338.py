
import time
from collections import deque
from threading import Lock


class RateLimiter:
    '''Simple rate limiter to ensure we don't exceed API rate limits.'''

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        '''
        Initialize the rate limiter.
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        '''
        self.max_calls = max_calls
        self.period = period
        self._calls = deque()
        self._lock = Lock()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self._lock:
            now = time.time()

            # Remove timestamps that are outside the period window
            while self._calls and now - self._calls[0] >= self.period:
                self._calls.popleft()

            if len(self._calls) < self.max_calls:
                # We can proceed immediately
                self._calls.append(now)
                return

            # Need to wait until the oldest call is outside the window
            earliest = self._calls[0]
            sleep_time = self.period - (now - earliest)
            if sleep_time > 0:
                time.sleep(sleep_time)

            # After sleeping, clean up again and record the call
            now = time.time()
            while self._calls and now - self._calls[0] >= self.period:
                self._calls.popleft()
            self._calls.append(now)
