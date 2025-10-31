
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
        self.timestamps = deque()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        now = time.time()
        while self.timestamps and now - self.timestamps[0] >= self.period:
            self.timestamps.popleft()

        if len(self.timestamps) >= self.max_calls:
            sleep_time = self.period - (now - self.timestamps[0])
            time.sleep(sleep_time)
            now = time.time()
            self.timestamps.popleft()

        self.timestamps.append(now)
