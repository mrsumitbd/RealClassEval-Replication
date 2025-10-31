
import time


class RateLimiter:

    def __init__(self, hz):
        self.hz = hz
        self.period = 1.0 / hz if hz > 0 else 0
        self._next_time = None

    def sleep(self, env):
        now = time.time()
        if self._next_time is None:
            self._next_time = now + self.period
            return
        sleep_time = self._next_time - now
        if sleep_time > 0:
            time.sleep(sleep_time)
        self._next_time += self.period
