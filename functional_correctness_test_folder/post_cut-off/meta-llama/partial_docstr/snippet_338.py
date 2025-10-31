
import time
from collections import deque


class RateLimiter:

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        '''
        Initialize the rate limiter.
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        '''
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        current_time = time.time()
        while self.calls and current_time - self.calls[0] > self.period:
            self.calls.popleft()

        if len(self.calls) >= self.max_calls:
            wait_time = self.calls[0] + self.period - current_time
            time.sleep(wait_time)
            self.calls.popleft()

        self.calls.append(current_time)
