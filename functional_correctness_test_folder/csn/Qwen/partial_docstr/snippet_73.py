
import time
import threading
from typing import Dict


class SentinelHubRateLimit:

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.next_request_times = [time.time()] * num_processes
        self.lock = threading.Lock()

    def register_next(self) -> float:
        with self.lock:
            current_time = time.time()
            next_time = min(self.next_request_times)
            wait_time = max(0, next_time - current_time)
            return wait_time

    def update(self, headers: Dict, *, default: float) -> None:
        with self.lock:
            retry_after = headers.get('Retry-After')
            if retry_after:
                try:
                    retry_after = float(retry_after)
                except ValueError:
                    retry_after = default / 1000.0
            else:
                retry_after = default / 1000.0

            retry_after = max(self.minimum_wait_time, min(
                retry_after, self.maximum_wait_time))
            current_time = time.time()
            for i in range(self.num_processes):
                if self.next_request_times[i] <= current_time:
                    self.next_request_times[i] = current_time + retry_after
                    break
