
import time
from collections import deque
from typing import Deque


class CommandRateLimiter:
    """
    A simple sliding‑window rate limiter.

    Parameters
    ----------
    max_calls : int, default 5
        Maximum number of calls allowed in the given period.
    period : float, default 60.0
        Time window in seconds.
    """

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls: int = max_calls
        self.period: float = period
        self._calls: Deque[float] = deque()

    def _purge_old(self) -> None:
        """Remove timestamps that are older than the sliding window."""
        now = time.monotonic()
        cutoff = now - self.period
        while self._calls and self._calls[0] <= cutoff:
            self._calls.popleft()

    def can_call(self) -> bool:
        """
        Check if a call can be made without exceeding the rate limit.
        If allowed, record the call.

        Returns
        -------
        bool
            True if call is allowed, False otherwise.
        """
        self._purge_old()
        if len(self._calls) < self.max_calls:
            self._calls.append(time.monotonic())
            return True
        return False

    def calls_remaining(self) -> int:
        """
        Get the number of calls remaining in the current period.

        Returns
        -------
        int
            Number of calls remaining.
        """
        self._purge_old()
        return max(0, self.max_calls - len(self._calls))

    def time_to_next_call(self) -> float:
        """
        Get the time in seconds until the next call is allowed.

        Returns
        -------
        float
            Seconds until next call is allowed, or 0 if calls are available now.
        """
        self._purge_old()
        if len(self._calls) < self.max_calls:
            return 0.0
        now = time.monotonic()
        oldest = self._calls[0]
        wait = self.period - (now - oldest)
        return max(0.0, wait)
