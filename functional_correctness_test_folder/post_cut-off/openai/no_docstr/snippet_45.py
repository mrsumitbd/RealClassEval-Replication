
import time
from typing import Optional


class TokenBucketRateLimiter:
    """
    A simple token bucket rate limiter.

    Parameters
    ----------
    tokens_per_second : int
        The rate at which tokens are added to the bucket.
    bucket_capacity : Optional[int], default None
        The maximum number of tokens the bucket can hold. If None, defaults to
        `tokens_per_second`.
    """

    def __init__(self, tokens_per_second: int, bucket_capacity: Optional[int] = None):
        if tokens_per_second <= 0:
            raise ValueError("tokens_per_second must be positive")
        self.tokens_per_second = float(tokens_per_second)
        self.bucket_capacity = float(
            bucket_capacity if bucket_capacity is not None else tokens_per_second)
        if self.bucket_capacity <= 0:
            raise ValueError("bucket_capacity must be positive")
        self._tokens = self.bucket_capacity
        self._last_refill = time.time()

    def _refill_tokens(self):
        """Replenish tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self._last_refill
        if elapsed <= 0:
            return
        added = elapsed * self.tokens_per_second
        self._tokens = min(self.bucket_capacity, self._tokens + added)
        self._last_refill = now

    def try_consume_token(self) -> bool:
        """
        Attempt to consume a single token.

        Returns
        -------
        bool
            True if a token was consumed, False otherwise.
        """
        self._refill_tokens()
        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return True
        return False

    def get_wait_time(self) -> float:
        """
        Get the time (in seconds) until the next token becomes available.

        Returns
        -------
        float
            Seconds to wait. Zero if a token is currently available.
        """
        self._refill_tokens()
        if self._tokens >= 1.0:
            return 0.0
        # Tokens needed to reach 1
        needed = 1.0 - self._tokens
        return needed / self.tokens_per_second
