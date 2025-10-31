
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
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()

        if len(self.calls) >= self.max_calls:
            sleep_time = self.period - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.calls.popleft()

        self.calls.append(now)
