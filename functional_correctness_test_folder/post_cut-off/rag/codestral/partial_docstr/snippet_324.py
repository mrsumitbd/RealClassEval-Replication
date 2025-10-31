
import time


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
        self.calls = []
        self.last_reset = time.time()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        self._reset_if_needed()
        return len(self.calls) < self.max_calls

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        self._reset_if_needed()
        return max(0, self.max_calls - len(self.calls))

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        self._reset_if_needed()
        if len(self.calls) < self.max_calls:
            return 0.0
        oldest_call_time = self.calls[0]
        time_since_oldest = time.time() - oldest_call_time
        return max(0.0, self.period - time_since_oldest)

    def _reset_if_needed(self):
        '''Reset the call counter if the period has elapsed.'''
        current_time = time.time()
        if current_time - self.last_reset >= self.period:
            self.calls = []
            self.last_reset = current_time
