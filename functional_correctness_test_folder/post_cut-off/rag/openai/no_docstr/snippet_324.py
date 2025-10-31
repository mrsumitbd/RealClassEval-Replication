
import time
from collections import deque
from typing import Deque


class CommandRateLimiter:
    '''Rate limiter for OVMS commands.
    Prevents sending too many commands in a short period to avoid overwhelming the OVMS module.
    '''

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        '''Initialize the rate limiter.
        Args:
            max_calls: Maximum number of calls allowed per period
            period: Time period in seconds
        '''
        if max_calls <= 0:
            raise ValueError("max_calls must be positive")
        if period <= 0:
            raise ValueError("period must be positive")
        self.max_calls: int = max_calls
        self.period: float = period
        self._calls: Deque[float] = deque()

    def _prune_old_calls(self) -> None:
        '''Remove timestamps older than the current period.'''
        now = time.monotonic()
        while self._calls and now - self._calls[0] > self.period:
            self._calls.popleft()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        self._prune_old_calls()
        if len(self._calls) < self.max_calls:
            self._calls.append(time.monotonic())
            return True
        return False

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        self._prune_old_calls()
        return max(0, self.max_calls - len(self._calls))

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        self._prune_old_calls()
        if len(self._calls) < self.max_calls:
            return 0.0
        now = time.monotonic()
        earliest = self._calls[0]
        wait = (earliest + self.period) - now
        return max(0.0, wait)
