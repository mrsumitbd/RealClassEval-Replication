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
        self.max_calls = max_calls
        self.period = period
        self._calls = []  # list of timestamps of recent calls

    def _purge_old_calls(self, now: float):
        '''Remove calls older than the period.'''
        cutoff = now - self.period
        while self._calls and self._calls[0] <= cutoff:
            self._calls.pop(0)

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        now = time.time()
        self._purge_old_calls(now)
        if len(self._calls) < self.max_calls:
            self._calls.append(now)
            return True
        return False

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        now = time.time()
        self._purge_old_calls(now)
        return max(0, self.max_calls - len(self._calls))

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        now = time.time()
        self._purge_old_calls(now)
        if len(self._calls) < self.max_calls:
            return 0.0
        earliest = self._calls[0]
        wait = self.period - (now - earliest)
        return max(0.0, wait)
