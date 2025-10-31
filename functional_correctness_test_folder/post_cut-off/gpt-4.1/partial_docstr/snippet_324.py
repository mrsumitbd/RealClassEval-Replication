
import time
from collections import deque


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def can_call(self) -> bool:
        now = time.time()
        # Remove calls outside the period window
        while self.calls and self.calls[0] <= now - self.period:
            self.calls.popleft()
        return len(self.calls) < self.max_calls

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
        # Time until the oldest call is outside the period window
        return max(0.0, self.calls[0] + self.period - now)

    # Optionally, a method to record a call
    def record_call(self):
        now = time.time()
        while self.calls and self.calls[0] <= now - self.period:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False
