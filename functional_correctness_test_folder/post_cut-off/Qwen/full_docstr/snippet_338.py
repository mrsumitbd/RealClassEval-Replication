
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
        self.calls = deque()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        current_time = time.time()
        # Remove calls from the deque that are outside the current period
        while self.calls and current_time - self.calls[0] > self.period:
            self.calls.popleft()

        # If the number of calls in the current period exceeds max_calls, wait
        if len(self.calls) >= self.max_calls:
            time.sleep(self.period - (current_time - self.calls[0]))

        # Record the current call
        self.calls.append(time.time())
