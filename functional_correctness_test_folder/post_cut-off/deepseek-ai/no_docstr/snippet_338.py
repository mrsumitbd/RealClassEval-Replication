
import time
from collections import deque


class RateLimiter:

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def wait(self):
        now = time.time()
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()
        if len(self.calls) >= self.max_calls:
            sleep_time = self.period - (now - self.calls[0])
            time.sleep(sleep_time)
            now = time.time()
            self.calls.popleft()
        self.calls.append(now)
