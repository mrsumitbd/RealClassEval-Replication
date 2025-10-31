
from time import time
from typing import Optional


class TokenBucketRateLimiter:

    def __init__(self, tokens_per_second: int, bucket_capacity: Optional[int] = None):
        self.tokens_per_second = tokens_per_second
        self.bucket_capacity = bucket_capacity if bucket_capacity is not None else tokens_per_second
        self.tokens = self.bucket_capacity
        self.last_refill_time = time()

    def _refill_tokens(self):
        current_time = time()
        elapsed_time = current_time - self.last_refill_time
        tokens_to_add = elapsed_time * self.tokens_per_second
        self.tokens = min(self.tokens + tokens_to_add, self.bucket_capacity)
        self.last_refill_time = current_time

    def try_consume_token(self) -> bool:
        self._refill_tokens()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def get_wait_time(self) -> float:
        self._refill_tokens()
        if self.tokens >= 1:
            return 0.0
        tokens_needed = 1 - self.tokens
        return tokens_needed / self.tokens_per_second
