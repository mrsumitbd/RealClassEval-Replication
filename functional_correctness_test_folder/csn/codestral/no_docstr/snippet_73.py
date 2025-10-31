
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
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.wait_time:
            time.sleep(self.wait_time - time_since_last_request)
        self.last_request_time = time.time()
        return self.wait_time

    def update(self, headers: Dict[str, str], *, default: float) -> None:
        if 'RateLimit-Reset' in headers:
            reset_time = float(headers['RateLimit-Reset'])
            current_time = time.time()
            if reset_time > current_time:
                self.wait_time = min(
                    max(reset_time - current_time, self.minimum_wait_time), self.maximum_wait_time)
            else:
                self.wait_time = self.minimum_wait_time
        else:
            self.wait_time = default
