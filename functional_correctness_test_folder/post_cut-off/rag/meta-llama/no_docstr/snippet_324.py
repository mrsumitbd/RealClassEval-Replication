
import time
from collections import deque


class CommandRateLimiter:
    """Rate limiter for OVMS commands.
    Prevents sending too many commands in a short period to avoid overwhelming the OVMS module.
    """

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        """Initialize the rate limiter.
        Args:
            max_calls: Maximum number of calls allowed per period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.call_timestamps = deque()

    def can_call(self) -> bool:
        """Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        """
        self._clean_up_old_calls()
        return len(self.call_timestamps) < self.max_calls

    def calls_remaining(self) -> int:
        """Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        """
        self._clean_up_old_calls()
        return self.max_calls - len(self.call_timestamps)

    def time_to_next_call(self) -> float:
        """Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        """
        self._clean_up_old_calls()
        if len(self.call_timestamps) < self.max_calls:
            return 0.0
        else:
            return max(0.0, self.call_timestamps[0] + self.period - time.time())

    def _clean_up_old_calls(self):
        current_time = time.time()
        while self.call_timestamps and self.call_timestamps[0] <= current_time - self.period:
            self.call_timestamps.popleft()
        if self.can_call():
            self.call_timestamps.append(current_time)
