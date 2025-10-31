
class ConstantDelayRetryPolicy:

    def __init__(self, maximum_attempts: int = 3, delay: float = 5) -> None:
        """
        Initializes a ConstantDelayRetryPolicy instance.

        Args:
        maximum_attempts (int): The maximum number of attempts to make before giving up. Defaults to 3.
        delay (float): The delay in seconds between attempts. Defaults to 5.
        """
        self.maximum_attempts = maximum_attempts
        self.delay = delay

    def next(self, elapsed_time: float, attempts: int, error: Exception) -> float | None:
        """
        Determines the next delay before retrying.

        Args:
        elapsed_time (float): The total elapsed time since the initial attempt.
        attempts (int): The number of attempts made so far.
        error (Exception): The exception that caused the current retry.

        Returns:
        float | None: The delay in seconds before the next attempt, or None if no further attempts should be made.
        """
        if attempts >= self.maximum_attempts:
            return None
        return self.delay
