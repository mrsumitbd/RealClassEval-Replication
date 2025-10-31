class ConstantDelayRetryPolicy:
    """Retry at a fixed interval up to a maximum number of attempts.

    Examples:
        ```python
        @step(retry_policy=ConstantDelayRetryPolicy(delay=5, maximum_attempts=10))
        async def flaky(self, ev: StartEvent) -> StopEvent:
            ...
        ```
    """

    def __init__(self, maximum_attempts: int=3, delay: float=5) -> None:
        """
        Initialize the policy.

        Args:
            maximum_attempts (int): Maximum consecutive attempts. Defaults to 3.
            delay (float): Seconds to wait between attempts. Defaults to 5.
        """
        self.maximum_attempts = maximum_attempts
        self.delay = delay

    def next(self, elapsed_time: float, attempts: int, error: Exception) -> float | None:
        """Return the fixed delay while attempts remain; otherwise `None`."""
        if attempts >= self.maximum_attempts:
            return None
        return self.delay