
import time
from typing import Dict


class SentinelHubRateLimit:
    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.last_request_time = time.time()
        self.request_count = 0
        self.unit_time = 1.0  # Assuming unit time is 1 second
        # Will be updated with actual value from headers
        self.max_requests = float('inf')

    def register_next(self) -> float:
        current_time = time.time()
        elapsed_time = current_time - self.last_request_time
        if elapsed_time > self.unit_time:
            self.request_count = 0
            self.last_request_time = current_time

        wait_time = max(0, (self.request_count + 1) *
                        self.unit_time / self.max_requests - elapsed_time)
        wait_time = max(self.minimum_wait_time, min(
            wait_time, self.maximum_wait_time))
        self.request_count += 1
        return wait_time

    def update(self, headers: Dict[str, str], *, default: float) -> None:
        try:
            self.max_requests = int(headers.get(
                'x-ratelimit-remaining', default))
            self.unit_time = int(headers.get('x-ratelimit-unit', 1))
        except ValueError:
            self.max_requests = default
