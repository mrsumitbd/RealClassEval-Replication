
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
        self.call_timestamps = deque()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        current_time = time.time()
        while self.call_timestamps and current_time - self.call_timestamps[0] > self.period:
            self.call_timestamps.popleft()

        if len(self.call_timestamps) >= self.max_calls:
            wait_time = self.call_timestamps[0] + self.period - current_time
            time.sleep(max(0, wait_time))

        self.call_timestamps.append(time.time())
