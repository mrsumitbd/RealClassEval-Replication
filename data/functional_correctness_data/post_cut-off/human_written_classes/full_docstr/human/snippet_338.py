import threading
import time

class RateLimiter:
    """Simple rate limiter to ensure we don't exceed API rate limits."""

    def __init__(self, max_calls: int=3, period: float=1.0):
        """
        Initialize the rate limiter.

        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()

    def wait(self):
        """
        Wait if necessary to respect the rate limit.
        """
        with self.lock:
            now = time.time()
            self.calls = [t for t in self.calls if now - t < self.period]
            if len(self.calls) >= self.max_calls:
                oldest_call = min(self.calls)
                wait_time = self.period - (now - oldest_call)
                if wait_time > 0:
                    time.sleep(wait_time)
                self.calls = []
            self.calls.append(time.time())