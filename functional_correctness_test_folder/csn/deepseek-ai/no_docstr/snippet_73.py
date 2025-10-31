
import time
from typing import Dict


class SentinelHubRateLimit:

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.last_request_time = 0.0
        self.wait_time = minimum_wait_time

    def register_next(self) -> float:
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        remaining_wait = max(0.0, self.wait_time - elapsed)

        if remaining_wait > 0:
            time.sleep(remaining_wait)

        self.last_request_time = time.time()
        return remaining_wait

    def update(self, headers: Dict, *, default: float) -> None:
        if 'X-RateLimit-Reset' in headers:
            reset_time = float(headers['X-RateLimit-Reset'])
            self.wait_time = max(self.minimum_wait_time, min(
                reset_time, self.maximum_wait_time))
        else:
            self.wait_time = max(self.minimum_wait_time, min(
                default, self.maximum_wait_time))
