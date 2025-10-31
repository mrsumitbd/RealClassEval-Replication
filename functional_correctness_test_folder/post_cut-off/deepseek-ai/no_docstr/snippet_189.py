
import time


class RateLimiter:

    def __init__(self, hz):
        self.period = 1.0 / hz
        self.last_time = time.time()

    def sleep(self, env):
        elapsed = time.time() - self.last_time
        sleep_time = max(0.0, self.period - elapsed)
        time.sleep(sleep_time)
        self.last_time = time.time()
