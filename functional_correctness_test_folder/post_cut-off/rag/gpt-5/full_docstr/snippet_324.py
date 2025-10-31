from collections import deque
from threading import Lock
from time import monotonic
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
            raise ValueError("max_calls must be > 0")
        if period <= 0:
            raise ValueError("period must be > 0")

        self.max_calls: int = int(max_calls)
        self.period: float = float(period)
        self._timestamps: Deque[float] = deque()
        self._lock = Lock()

    def _prune(self, now: float) -> None:
        while self._timestamps and (now - self._timestamps[0]) >= self.period:
            self._timestamps.popleft()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        now = monotonic()
        with self._lock:
            self._prune(now)
            if len(self._timestamps) < self.max_calls:
                self._timestamps.append(now)
                return True
            return False

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        now = monotonic()
        with self._lock:
            self._prune(now)
            return self.max_calls - len(self._timestamps)

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        now = monotonic()
        with self._lock:
            self._prune(now)
            if len(self._timestamps) < self.max_calls:
                return 0.0
            oldest = self._timestamps[0]
            wait = self.period - (now - oldest)
            return max(0.0, wait)
