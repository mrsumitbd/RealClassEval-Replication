
import time


class RateLimiter:

    def __init__(self, hz):
        self.hz = hz
        self.interval = 1.0 / hz
        self.last_call = time.time()

    def sleep(self, env):
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()
