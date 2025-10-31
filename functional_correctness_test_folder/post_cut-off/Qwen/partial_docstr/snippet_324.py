
import time
from collections import deque


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def can_call(self) -> bool:
        self._cleanup()
        return len(self.calls) < self.max_calls

    def calls_remaining(self) -> int:
        self._cleanup()
        return self.max_calls - len(self.calls)

    def time_to_next_call(self) -> float:
        self._cleanup()
        if len(self.calls) < self.max_calls:
            return 0.0
        next_call_time = self.calls[0] + self.period
        return max(0.0, next_call_time - time.time())

    def _cleanup(self):
        current_time = time.time()
        while self.calls and self.calls[0] < current_time - self.period:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            self.calls.append(current_time)
