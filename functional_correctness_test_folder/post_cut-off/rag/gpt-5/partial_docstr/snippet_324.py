from collections import deque
from threading import Lock
from time import monotonic


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
            raise ValueError("max_calls must be a positive integer")
        if period <= 0:
            raise ValueError("period must be a positive number of seconds")
        self.max_calls = int(max_calls)
        self.period = float(period)
        self._calls = deque()  # stores timestamps (monotonic) of recent calls
        self._lock = Lock()

    def _prune(self, now: float) -> None:
        while self._calls and (now - self._calls[0]) >= self.period:
            self._calls.popleft()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        now = monotonic()
        with self._lock:
            self._prune(now)
            if len(self._calls) < self.max_calls:
                self._calls.append(now)
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
            remaining = self.max_calls - len(self._calls)
            return remaining if remaining > 0 else 0

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        now = monotonic()
        with self._lock:
            self._prune(now)
            if len(self._calls) < self.max_calls:
                return 0.0
            oldest = self._calls[0]
            wait = self.period - (now - oldest)
            return wait if wait > 0 else 0.0
