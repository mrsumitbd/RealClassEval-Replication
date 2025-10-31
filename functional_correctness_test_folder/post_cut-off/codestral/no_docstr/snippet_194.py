
class ConstantDelayRetryPolicy:

    def __init__(self, maximum_attempts: int = 3, delay: float = 5) -> None:
        self.maximum_attempts = maximum_attempts
        self.delay = delay

    def next(self, elapsed_time: float, attempts: int, error: Exception) -> float | None:
        if attempts < self.maximum_attempts:
            return self.delay
        return None
