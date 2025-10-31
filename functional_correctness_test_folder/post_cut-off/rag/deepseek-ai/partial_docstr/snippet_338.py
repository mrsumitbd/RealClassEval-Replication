
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
        self.timestamps = deque(maxlen=max_calls)

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        now = time.time()
        if len(self.timestamps) >= self.max_calls:
            oldest = self.timestamps[0]
            elapsed = now - oldest
            if elapsed < self.period:
                time.sleep(self.period - elapsed)
        self.timestamps.append(time.time())
