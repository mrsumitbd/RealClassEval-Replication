class ConstantDelayRetryPolicy:

    def __init__(self, maximum_attempts: int = 3, delay: float = 5) -> None:
        if not isinstance(maximum_attempts, int):
            raise TypeError("maximum_attempts must be an int")
        if maximum_attempts < 0:
            raise ValueError("maximum_attempts must be >= 0")
        if not isinstance(delay, (int, float)):
            raise TypeError("delay must be a number")
        if delay < 0:
            raise ValueError("delay must be >= 0")
        self.maximum_attempts = maximum_attempts
        self.delay = float(delay)

    def next(self, elapsed_time: float, attempts: int, error: Exception) -> float | None:
        if attempts >= self.maximum_attempts:
            return None
        return self.delay
