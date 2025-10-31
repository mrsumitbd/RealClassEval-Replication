import time
from collections import deque
from typing import Deque


class CommandRateLimiter:
    def __init__(self, max_calls: int = 5, period: float = 60.0):
        if not isinstance(max_calls, int) or max_calls <= 0:
            raise ValueError("max_calls must be a positive integer")
        if not isinstance(period, (int, float)) or period <= 0:
            raise ValueError("period must be a positive number")
        self.max_calls = max_calls
        self.period = float(period)
        self._calls: Deque[float] = deque()

    def _prune(self, now: float) -> None:
        cutoff = now - self.period
        while self._calls and self._calls[0] <= cutoff:
            self._calls.popleft()

    def can_call(self) -> bool:
        now = time.monotonic()
        self._prune(now)
        if len(self._calls) < self.max_calls:
            self._calls.append(now)
            return True
        return False

    def calls_remaining(self) -> int:
        now = time.monotonic()
        self._prune(now)
        return max(0, self.max_calls - len(self._calls))

    def time_to_next_call(self) -> float:
        now = time.monotonic()
        self._prune(now)
        if len(self._calls) < self.max_calls:
            return 0.0
        oldest = self._calls[0]
        return max(0.0, self.period - (now - oldest))
