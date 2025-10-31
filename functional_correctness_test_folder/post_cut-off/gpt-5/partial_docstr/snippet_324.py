from collections import deque
import time
import threading


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = int(max_calls)
        self.period = float(period)
        self._calls = deque()
        self._lock = threading.Lock()

    def _purge_old(self, now: float) -> None:
        cutoff = now - self.period
        while self._calls and self._calls[0] <= cutoff:
            self._calls.popleft()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        now = time.monotonic()
        with self._lock:
            self._purge_old(now)
            if len(self._calls) < self.max_calls:
                self._calls.append(now)
                return True
            return False

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        now = time.monotonic()
        with self._lock:
            self._purge_old(now)
            remaining = self.max_calls - len(self._calls)
            return remaining if remaining > 0 else 0

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        now = time.monotonic()
        with self._lock:
            self._purge_old(now)
            if len(self._calls) < self.max_calls:
                return 0.0
            return max(0.0, (self._calls[0] + self.period) - now)
