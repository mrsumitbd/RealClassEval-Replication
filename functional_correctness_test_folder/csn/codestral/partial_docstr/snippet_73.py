
import time
import math


class SentinelHubRateLimit:

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.next_possible_download_time = time.time()

    def register_next(self) -> float:
        current_time = time.time()
        if current_time < self.next_possible_download_time:
            time.sleep(self.next_possible_download_time - current_time)
        self.next_possible_download_time = time.time() + self.minimum_wait_time * \
            self.num_processes
        return self.next_possible_download_time

    def update(self, headers: dict, *, default: float) -> None:
        if 'Retry-After' in headers:
            retry_after = float(headers['Retry-After'])
            self.next_possible_download_time = time.time() + retry_after
        else:
            self.next_possible_download_time = time.time() + default / 1000.0
        self.next_possible_download_time = max(self.next_possible_download_time, time.time(
        ) + self.minimum_wait_time * self.num_processes)
        self.next_possible_download_time = min(
            self.next_possible_download_time, time.time() + self.maximum_wait_time)
