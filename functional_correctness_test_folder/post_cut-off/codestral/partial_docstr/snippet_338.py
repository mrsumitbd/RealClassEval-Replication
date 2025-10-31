
import time


class RateLimiter:

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.last_reset = time.time()

    def wait(self):
        current_time = time.time()
        if current_time - self.last_reset > self.period:
            self.calls = []
            self.last_reset = current_time
        if len(self.calls) >= self.max_calls:
            time_to_wait = self.last_reset + self.period - current_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            self.calls = []
            self.last_reset = time.time()
        self.calls.append(current_time)
