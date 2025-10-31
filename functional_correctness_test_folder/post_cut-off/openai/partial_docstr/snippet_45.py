
import time
from typing import Optional


class TokenBucketRateLimiter:
    def __init__(self, tokens_per_second: int, bucket_capacity: Optional[int] = None):
        """
        Initialize token bucket rate limiter.

        Args:
            tokens_per_second: Rate at which tokens are refilled.
            bucket_capacity: Maximum number of tokens in bucket (defaults to tokens_per_second).
        """
        self.tokens_per_second = float(tokens_per_second)
        self.bucket_capacity = float(
            bucket_capacity if bucket_capacity is not None else tokens_per_second)
        self._current_tokens = self.bucket_capacity
        self._last_refill = time.monotonic()

    def _refill_tokens(self):
        """Refill tokens based on time elapsed since last refill."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        if elapsed <= 0:
            return
        added = elapsed * self.tokens_per_second
        self._current_tokens = min(
            self.bucket_capacity, self._current_tokens + added)
        self._last_refill = now

    def try_consume_token(self) -> bool:
        """
        Try to consume a token from the bucket.

        Returns:
            True if token was consumed, False if bucket is empty.
        """
        self._refill_tokens()
        if self._current_tokens >= 1.0:
            self._current_tokens -= 1.0
            return True
        return False

    def get_wait_time(self) -> float:
        """
        Calculate how long to wait before a token will be available.

        Returns:
            Time in seconds to wait.
        """
        self._refill_tokens()
        if self._current_tokens >= 1.0:
            return 0.0
        needed = 1.0 - self._current_tokens
        return needed / self.tokens_per_second
