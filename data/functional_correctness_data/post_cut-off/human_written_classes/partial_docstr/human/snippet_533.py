import logging
import threading
import random
import time

class RateLimiter:
    """
    Thread-safe rate limiter that controls the frequency of requests.
    """

    def __init__(self, rate_limit: int=2):
        self.rate_limit = rate_limit
        self.logger = logging.getLogger(__name__)
        self.request_timestamps: list[float] = []
        self.waiting_requests_count = 0
        self._lock = threading.Lock()

    def apply_rate_limiting(self):
        if self.rate_limit <= 0:
            return
        with self._lock:
            current_time = time.time()
            self.request_timestamps = [ts for ts in self.request_timestamps if current_time - ts < 1.0]
            if len(self.request_timestamps) >= self.rate_limit:
                self.waiting_requests_count += 1
                sleep_time = self.waiting_requests_count / self.rate_limit * 1.0 - (current_time - self.request_timestamps[0]) + random.uniform(0, 1)
                if sleep_time > 0:
                    self.logger.debug(f'Exceed rate limit, retry in {sleep_time} seconds...')
                    time.sleep(sleep_time)
            self.waiting_requests_count -= 1
            if self.waiting_requests_count < 0:
                self.waiting_requests_count = 0
            self.request_timestamps.append(time.time())