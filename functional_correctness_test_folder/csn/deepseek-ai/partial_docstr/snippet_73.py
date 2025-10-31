
import time
from typing import Dict, Optional


class SentinelHubRateLimit:

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.next_request_time = 0.0
        self.last_request_time = 0.0

    def register_next(self) -> float:
        current_time = time.time()
        wait_time = max(0.0, self.next_request_time - current_time)
        self.last_request_time = current_time + wait_time
        self.next_request_time = self.last_request_time + self.minimum_wait_time
        return wait_time

    def update(self, headers: Dict, *, default: float) -> None:
        current_time = time.time()
        retry_after = self._parse_retry_after(headers, default)

        next_possible_time = current_time + retry_after
        if next_possible_time > self.next_request_time:
            self.next_request_time = next_possible_time

    def _parse_retry_after(self, headers: Dict, default: float) -> float:
        retry_after = headers.get("Retry-After")
        if retry_after is None:
            return default / 1000.0

        try:
            return float(retry_after)
        except ValueError:
            pass

        try:
            from email.utils import parsedate_to_datetime
            retry_date = parsedate_to_datetime(retry_after)
            return (retry_date.timestamp() - time.time())
        except (TypeError, ValueError):
            return default / 1000.0
