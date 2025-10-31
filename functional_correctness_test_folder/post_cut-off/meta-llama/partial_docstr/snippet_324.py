
import time
from collections import deque


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.call_timestamps = deque()

    def can_call(self) -> bool:
        '''Check if a call can be made without exceeding the rate limit.
        Returns:
            True if call is allowed, False if limit would be exceeded
        '''
        self._clean_call_timestamps()
        return len(self.call_timestamps) < self.max_calls

    def calls_remaining(self) -> int:
        '''Get the number of calls remaining in the current period.
        Returns:
            Number of calls remaining
        '''
        self._clean_call_timestamps()
        return self.max_calls - len(self.call_timestamps)

    def time_to_next_call(self) -> float:
        '''Get the time in seconds until the next call is allowed.
        Returns:
            Seconds until next call is allowed, or 0 if calls are available now
        '''
        self._clean_call_timestamps()
        if len(self.call_timestamps) < self.max_calls:
            return 0.0
        else:
            return max(0.0, self.call_timestamps[0] + self.period - time.time())

    def _clean_call_timestamps(self):
        current_time = time.time()
        while self.call_timestamps and self.call_timestamps[0] <= current_time - self.period:
            self.call_timestamps.popleft()
        if self.can_call():
            self.call_timestamps.append(current_time)


# Example usage:
if __name__ == "__main__":
    limiter = CommandRateLimiter(max_calls=5, period=60.0)
    for _ in range(10):
        if limiter.can_call():
            print("Call allowed")
            # manually trigger timestamp update for demonstration
            limiter._clean_call_timestamps()
        else:
            print(
                f"Call not allowed. Time to next call: {limiter.time_to_next_call()} seconds")
            print(f"Calls remaining: {limiter.calls_remaining()}")
        time.sleep(1)
