
import time
import threading
from collections import deque


class RateLimiter:

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            now = time.monotonic()
            while self.calls and self.calls[0] <= now - self.period:
                self.calls.popleft()
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return
            else:
                earliest = self.calls[0]
                wait_time = earliest + self.period - now
                if wait_time > 0:
                    time.sleep(wait_time)
                # After sleeping, remove old calls and append new one
                now = time.monotonic()
                while self.calls and self.calls[0] <= now - self.period:
                    self.calls.popleft()
                self.calls.append(now)
