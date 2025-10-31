
import time
import threading


class RateLimiter:
    def __init__(self, max_calls: int = 3, period: float = 1.0):
        """
        Initialize the rate limiter.

        Args:
            max_calls: Maximum number of calls allowed in the period.
            period: Time period in seconds.
        """
        self.max_calls = max_calls
        self.period = period
        self._calls = []          # timestamps of recent calls
        self._lock = threading.Lock()

    def wait(self):
        """
        Wait if necessary to respect the rate limit.
        """
        with self._lock:
            now = time.monotonic()
            # Remove timestamps older than the period
            while self._calls and self._calls[0] <= now - self.period:
                self._calls.pop(0)

            if len(self._calls) < self.max_calls:
                # We can proceed immediately
                self._calls.append(now)
                return

            # Need to wait until the oldest call is outside the period
            earliest = self._calls[0]
            wait_time = (earliest + self.period) - now

        if wait_time > 0:
            time.sleep(wait_time)

        # After sleeping, record the new call timestamp
        with self._lock:
            now = time.monotonic()
            while self._calls and self._calls[0] <= now - self.period:
                self._calls.pop(0)
            self._calls.append(now)
