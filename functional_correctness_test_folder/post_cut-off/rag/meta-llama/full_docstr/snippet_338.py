
import time
from collections import deque


class RateLimiter:
    """Simple rate limiter to ensure we don't exceed API rate limits."""

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        """
        Initialize the rate limiter.

        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def wait(self):
        """
        Wait if necessary to respect the rate limit.
        """
        now = time.time()
        self.calls.append(now)
        while len(self.calls) > self.max_calls:
            oldest_call = self.calls.popleft()
            if now - oldest_call < self.period:
                time_to_wait = self.period - (now - oldest_call)
                time.sleep(time_to_wait)
                now = time.time()
            else:
                break
