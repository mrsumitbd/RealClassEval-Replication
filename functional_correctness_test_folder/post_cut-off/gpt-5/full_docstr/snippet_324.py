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
        import threading
        from collections import deque
        self.max_calls = int(max(0, max_calls))
        self.period = float(max(0.0, period))
        self._calls = deque()
        self._lock = threading.Lock()
        # Use monotonic for timekeeping
        import time
        self._time = time.monotonic

    def _evict_expired(self, now: float) -> None:
        if self.period <= 0:
            # If period is zero, only allow up to max_calls instantly; then immediately expire all
            self._calls.clear()
            return
        cutoff = now - self.period
        dq = self._calls
        while dq and dq[0] <= cutoff:
            dq.popleft()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        if self.max_calls <= 0:
            return False
        now = self._time()
        with self._lock:
            self._evict_expired(now)
            if len(self._calls) < self.max_calls:
                self._calls.append(now)
                return True
            return False

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        if self.max_calls <= 0:
            return 0
        now = self._time()
        with self._lock:
            self._evict_expired(now)
            remaining = self.max_calls - len(self._calls)
            return remaining if remaining > 0 else 0

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        if self.max_calls <= 0:
            return float('inf')
        now = self._time()
        with self._lock:
            self._evict_expired(now)
            if len(self._calls) < self.max_calls:
                return 0.0
            if not self._calls:
                return 0.0
            if self.period <= 0:
                return 0.0
            oldest = self._calls[0]
            wait = (oldest + self.period) - now
            return wait if wait > 0 else 0.0
