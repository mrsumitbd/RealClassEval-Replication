
import time
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
        self.calls = deque()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        self._remove_old_calls()
        return len(self.calls) < self.max_calls

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        self._remove_old_calls()
        return self.max_calls - len(self.calls)

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        self._remove_old_calls()
        if len(self.calls) < self.max_calls:
            return 0
        next_call_time = self.calls[0] + self.period
        return max(0, next_call_time - time.time())

    def _remove_old_calls(self):
        '''Remove calls from the deque that are outside the current period.'''
        current_time = time.time()
        while self.calls and self.calls[0] < current_time - self.period:
            self.calls.popleft()

    def call_made(self):
        '''Record that a call has been made.'''
        self.calls.append(time.time())
