
import time
from collections import deque
from typing import Deque


class CommandRateLimiter:
    """
    A simple rate limiter that allows at most `max_calls` calls within a sliding
    window of `period` seconds.
    """

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        if max_calls <= 0:
            raise ValueError("max_calls must be positive")
        if period <= 0:
            raise ValueError("period must be positive")

        self.max_calls: int = max_calls
        self.period: float = period
        self._calls: Deque[float] = deque()

    def _prune_old_calls(self) -> None:
        """Remove timestamps older than the sliding window."""
        now = time.monotonic()
        cutoff = now - self.period
        while self._calls and self._calls[0] <= cutoff:
            self._calls.popleft()

    def can_call(self) -> bool:
        """
        Return True if a new call is allowed at this moment.
        If allowed, record the call timestamp.
        """
        self._prune_old_calls()
        if len(self._calls) < self.max_calls:
            self._calls.append(time.monotonic())
            return True
        return False

    def calls_remaining(self) -> int:
        """
        Return the number of calls still allowed in the current window.
        """
        self._prune_old_calls()
        return max(0, self.max_calls - len(self._calls))

    def time_to_next_call(self) -> float:
        """
        Return the number of seconds until the next call is allowed.
        If a call is currently allowed, returns 0.0.
        """
        self._prune_old_calls()
        if len(self._calls) < self.max_calls:
            return 0.0
        # The earliest call that will expire
        earliest = self._calls[0]
        return max(0.0, (earliest + self.period) - time.monotonic())
