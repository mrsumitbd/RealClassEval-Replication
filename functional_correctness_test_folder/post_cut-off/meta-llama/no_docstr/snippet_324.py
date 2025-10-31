
import time
from collections import deque


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.call_timestamps = deque()

    def can_call(self) -> bool:
        self._clean_call_timestamps()
        return len(self.call_timestamps) < self.max_calls

    def calls_remaining(self) -> int:
        self._clean_call_timestamps()
        return self.max_calls - len(self.call_timestamps)

    def time_to_next_call(self) -> float:
        self._clean_call_timestamps()
        if len(self.call_timestamps) < self.max_calls:
            return 0.0
        else:
            return max(0.0, self.call_timestamps[0] + self.period - time.time())

    def _clean_call_timestamps(self):
        current_time = time.time()
        while self.call_timestamps and self.call_timestamps[0] <= current_time - self.period:
            self.call_timestamps.popleft()

    # To make the class more useful, we can add a call method that also records the call timestamp
    def call(self):
        if self.can_call():
            self.call_timestamps.append(time.time())
            return True
        else:
            return False


# Example usage:
if __name__ == "__main__":
    limiter = CommandRateLimiter(max_calls=5, period=60.0)
    for _ in range(10):
        if limiter.call():
            print("Call made")
        else:
            print(
                f"Rate limit exceeded. Time to next call: {limiter.time_to_next_call()} seconds")
        time.sleep(1)
