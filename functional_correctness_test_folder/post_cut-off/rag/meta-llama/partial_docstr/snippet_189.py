
import time


class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        """
        Args:
            hz (int): frequency to enforce
        """
        self.hz = hz
        self.last_time = time.time()

    def sleep(self, env=None):
        """Attempt to sleep at the specified rate in hz."""
        now = time.time()
        elapsed = now - self.last_time
        expected = 1.0 / self.hz
        if elapsed < expected:
            time.sleep(expected - elapsed)
        self.last_time = time.time()
