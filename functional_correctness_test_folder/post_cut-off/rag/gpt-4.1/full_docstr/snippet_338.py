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
        self.max_calls = max_calls
        self.period = period
        self.lock = threading.Lock()
        self.calls = deque()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self.lock:
            now = time.monotonic()
            while self.calls and self.calls[0] <= now - self.period:
                self.calls.popleft()
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return
            earliest = self.calls[0]
            wait_time = earliest + self.period - now
            if wait_time > 0:
                time.sleep(wait_time)
            # After sleeping, clean up and record the call
            now = time.monotonic()
            while self.calls and self.calls[0] <= now - self.period:
                self.calls.popleft()
            self.calls.append(now)
