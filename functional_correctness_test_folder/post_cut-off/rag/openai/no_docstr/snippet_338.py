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
        self.max_calls = max_calls
        self.period = period
        self._calls = deque()
        self._lock = threading.Lock()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self._lock:
            now = time.time()
            # Remove calls that are outside the window
            while self._calls and now - self._calls[0] >= self.period:
                self._calls.popleft()

            if len(self._calls) >= self.max_calls:
                # Need to wait until the oldest call falls out of the window
                oldest = self._calls[0]
                wait_time = self.period - (now - oldest)
                if wait_time > 0:
                    time.sleep(wait_time)
                # After sleeping, clean up again
                now = time.time()
                while self._calls and now - self._calls[0] >= self.period:
                    self._calls.popleft()

            # Record the current call
            self._calls.append(time.time())
