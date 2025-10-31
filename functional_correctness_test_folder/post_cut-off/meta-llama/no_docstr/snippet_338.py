
import time
from collections import deque


class RateLimiter:

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        self.max_calls = max_calls
        self.period = period
        self.call_timestamps = deque()

    def wait(self):
        current_time = time.time()
        while self.call_timestamps and current_time - self.call_timestamps[0] > self.period:
            self.call_timestamps.popleft()

        if len(self.call_timestamps) >= self.max_calls:
            sleep_time = self.call_timestamps[0] + self.period - current_time
            time.sleep(sleep_time)
            self.call_timestamps.popleft()

        self.call_timestamps.append(time.time())
