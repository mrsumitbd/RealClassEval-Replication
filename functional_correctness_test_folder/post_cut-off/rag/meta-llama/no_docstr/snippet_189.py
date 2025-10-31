
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

    def sleep(self):
        """Attempt to sleep at the specified rate in hz."""
        now = time.time()
        elapsed = now - self.last_time
        expected_elapsed = 1.0 / self.hz
        if elapsed < expected_elapsed:
            time.sleep(expected_elapsed - elapsed)
        self.last_time = time.time()
