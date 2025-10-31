
import time
from collections import deque


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def can_call(self) -> bool:
        self._remove_old_calls()
        return len(self.calls) < self.max_calls

    def calls_remaining(self) -> int:
        self._remove_old_calls()
        return self.max_calls - len(self.calls)

    def time_to_next_call(self) -> float:
        self._remove_old_calls()
        if len(self.calls) < self.max_calls:
            return 0.0
        return self.period - (time.time() - self.calls[0])

    def _remove_old_calls(self):
        current_time = time.time()
        while self.calls and current_time - self.calls[0] > self.period:
            self.calls.popleft()

    def register_call(self):
        self._remove_old_calls()
        if len(self.calls) < self.max_calls:
            self.calls.append(time.time())
