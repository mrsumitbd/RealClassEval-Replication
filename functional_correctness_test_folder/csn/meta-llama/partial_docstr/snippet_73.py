
import time
from typing import Dict


class SentinelHubRateLimit:
    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        '''
        :param num_processes: Number of parallel download processes running.
        :param minimum_wait_time: Minimum wait time between two consecutive download requests in seconds.
        :param maximum_wait_time: Maximum wait time between two consecutive download requests in seconds.
        '''
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.next_download_times = [time.time()] * num_processes

    def register_next(self) -> float:
        current_time = time.time()
        next_download_time = min(self.next_download_times)
        wait_time = max(next_download_time - current_time,
                        self.minimum_wait_time)
        self.next_download_times[self.next_download_times.index(
            next_download_time)] = current_time + wait_time
        return wait_time

    def update(self, headers: Dict[str, str], *, default: float) -> None:
        '''Update the next possible download time if the service has responded with the rate limit.
        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        '''
        try:
            retry_after = float(headers.get('Retry-After', 0))
            wait_time = max(
                retry_after, self.minimum_wait_time, default / 1000)
            wait_time = min(wait_time, self.maximum_wait_time)
        except ValueError:
            wait_time = max(self.minimum_wait_time, default / 1000)
            wait_time = min(wait_time, self.maximum_wait_time)

        next_download_time = min(self.next_download_times)
        self.next_download_times[self.next_download_times.index(
            next_download_time)] = max(next_download_time, time.time() + wait_time)
