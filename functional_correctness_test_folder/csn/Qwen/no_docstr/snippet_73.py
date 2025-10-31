
import time
import random


class SentinelHubRateLimit:

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.last_request_time = [0.0] * num_processes
        self.wait_time = minimum_wait_time

    def register_next(self) -> float:
        current_time = time.time()
        process_index = random.randint(0, self.num_processes - 1)
        next_request_time = self.last_request_time[process_index] + \
            self.wait_time
        wait_duration = max(0, next_request_time - current_time)
        time.sleep(wait_duration)
        self.last_request_time[process_index] = time.time()
        return wait_duration

    def update(self, headers: dict, *, default: float) -> None:
        retry_after = headers.get('Retry-After', default)
        try:
            self.wait_time = float(retry_after)
        except ValueError:
            self.wait_time = default
        self.wait_time = max(self.minimum_wait_time, min(
            self.wait_time, self.maximum_wait_time))
