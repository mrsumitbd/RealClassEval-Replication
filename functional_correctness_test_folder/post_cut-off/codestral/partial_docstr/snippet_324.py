
import time


class CommandRateLimiter:

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.last_reset = time.time()

    def can_call(self) -> bool:
        current_time = time.time()
        if current_time - self.last_reset > self.period:
            self.calls = []
            self.last_reset = current_time
        return len(self.calls) < self.max_calls

    def calls_remaining(self) -> int:
        current_time = time.time()
        if current_time - self.last_reset > self.period:
            self.calls = []
            self.last_reset = current_time
        return self.max_calls - len(self.calls)

    def time_to_next_call(self) -> float:
        current_time = time.time()
        if current_time - self.last_reset > self.period:
            self.calls = []
            self.last_reset = current_time
        if len(self.calls) < self.max_calls:
            return 0.0
        else:
            return self.period - (current_time - self.last_reset)
