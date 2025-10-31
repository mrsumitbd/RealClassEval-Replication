
import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        self.period = 1.0 / hz
        self.last_time = time.time()

    def sleep(self):
        elapsed = time.time() - self.last_time
        remaining = self.period - elapsed
        if remaining > 0:
            time.sleep(remaining)
        self.last_time = time.time()
