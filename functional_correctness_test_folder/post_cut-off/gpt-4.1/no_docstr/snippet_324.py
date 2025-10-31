
import time
import collections


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = collections.deque()

    def can_call(self) -> bool:
        now = time.time()
        while self.calls and self.calls[0] <= now - self.period:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

    def calls_remaining(self) -> int:
        now = time.time()
        while self.calls and self.calls[0] <= now - self.period:
            self.calls.popleft()
        return self.max_calls - len(self.calls)

    def time_to_next_call(self) -> float:
        now = time.time()
        while self.calls and self.calls[0] <= now - self.period:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            return 0.0
        return self.period - (now - self.calls[0])
