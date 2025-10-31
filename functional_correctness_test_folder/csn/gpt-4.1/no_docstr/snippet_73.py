
import time
import threading


class SentinelHubRateLimit:

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        self.num_processes = max(1, num_processes)
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.lock = threading.Lock()
        self.last_time = 0.0
        self.wait_time = minimum_wait_time

    def register_next(self) -> float:
        with self.lock:
            now = time.time()
            next_time = max(self.last_time + self.wait_time, now)
            wait = max(0.0, next_time - now)
            self.last_time = next_time
        if wait > 0:
            time.sleep(wait)
        return wait

    def update(self, headers: dict, *, default: float) -> None:
        # Try to get rate limit info from headers
        try:
            limit = int(headers.get("x-ratelimit-limit", 0))
            remaining = int(headers.get("x-ratelimit-remaining", 0))
            reset = float(headers.get("x-ratelimit-reset", 0))
        except Exception:
            limit = 0
            remaining = 0
            reset = 0.0

        with self.lock:
            if limit > 0 and remaining >= 0 and reset > 0:
                # Calculate wait time per process
                per_process_limit = max(1, limit // self.num_processes)
                per_process_remaining = max(1, remaining // self.num_processes)
                time_per_request = reset / max(1, per_process_remaining)
                self.wait_time = min(
                    max(time_per_request, self.minimum_wait_time), self.maximum_wait_time)
            else:
                self.wait_time = min(
                    max(default, self.minimum_wait_time), self.maximum_wait_time)
