
import time
from collections import deque


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.call_times = deque()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        self._cleanup()
        return len(self.call_times) < self.max_calls

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        self._cleanup()
        return max(0, self.max_calls - len(self.call_times))

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        self._cleanup()
        if len(self.call_times) < self.max_calls:
            return 0.0
        current_time = time.time()
        oldest_call = self.call_times[0]
        time_elapsed = current_time - oldest_call
        return max(0.0, self.period - time_elapsed)

    def _cleanup(self):
        current_time = time.time()
        while self.call_times and current_time - self.call_times[0] > self.period:
            self.call_times.popleft()
