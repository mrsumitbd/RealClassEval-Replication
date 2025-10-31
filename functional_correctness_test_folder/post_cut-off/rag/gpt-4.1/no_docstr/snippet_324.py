import time
import threading
from collections import deque


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
        self.max_calls = max_calls
        self.period = period
        self._lock = threading.Lock()
        self._call_times = deque()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        with self._lock:
            now = time.time()
            self._prune_old(now)
            return len(self._call_times) < self.max_calls

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        with self._lock:
            now = time.time()
            self._prune_old(now)
            return max(0, self.max_calls - len(self._call_times))

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        with self._lock:
            now = time.time()
            self._prune_old(now)
            if len(self._call_times) < self.max_calls:
                return 0.0
            oldest = self._call_times[0]
            return max(0.0, oldest + self.period - now)

    def _prune_old(self, now: float):
        while self._call_times and self._call_times[0] <= now - self.period:
            self._call_times.popleft()

    def record_call(self):
        '''Record a call occurrence. Should be called after a successful can_call().'''
        with self._lock:
            now = time.time()
            self._prune_old(now)
            self._call_times.append(now)
