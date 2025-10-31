
import time
from collections import deque


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.call_times = deque()

    def can_call(self) -> bool:
        current_time = time.time()
        while self.call_times and current_time - self.call_times[0] > self.period:
            self.call_times.popleft()
        return len(self.call_times) < self.max_calls

    def calls_remaining(self) -> int:
        current_time = time.time()
        while self.call_times and current_time - self.call_times[0] > self.period:
            self.call_times.popleft()
        return self.max_calls - len(self.call_times)

    def time_to_next_call(self) -> float:
        current_time = time.time()
        while self.call_times and current_time - self.call_times[0] > self.period:
            self.call_times.popleft()
        if len(self.call_times) < self.max_calls:
            return 0.0
        else:
            return self.period - (current_time - self.call_times[0])
