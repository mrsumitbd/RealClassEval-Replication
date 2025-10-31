
import time


class RateLimiter:

    def __init__(self, hz):
        self.period = 1.0 / hz
        self.last_time = time.time()

    def sleep(self, env):
        current_time = time.time()
        elapsed = current_time - self.last_time
        if elapsed < self.period:
            time.sleep(self.period - elapsed)
        self.last_time = time.time()
