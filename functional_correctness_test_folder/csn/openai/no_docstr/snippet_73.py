
import time
import threading
from typing import Dict, Any


class SentinelHubRateLimit:
    """
    Simple rate‑limiter for Sentinel‑Hub API calls.

    The limiter keeps track of the time that must elapse between consecutive
    requests.  The waiting period can be updated based on HTTP response
    headers (e.g. `Retry-After`).  The class is thread‑safe and can be used
    by multiple processes or threads.
    """

    def __init__(self, num_processes: int = 1,
                 minimum_wait_time: float = 0.05,
                 maximum_wait_time: float = 60.0):
        """
        Parameters
        ----------
        num_processes : int, optional
            Number of concurrent processes that will use the limiter.
            Currently unused but kept for API compatibility.
        minimum_wait_time : float, optional
            Minimum number of seconds to wait between requests.
        maximum_wait_time : float, optional
            Maximum number of seconds to wait between requests.
        """
        self.num_processes = max(1, int(num_processes))
        self.min_wait = float(minimum_wait_time)
        self.max_wait = float(maximum_wait_time)
        self._wait_time = self.min_wait
        self._last_call = 0.0
        self._lock = threading.Lock()

    def register_next(self) -> float:
        """
        Register the next request and return the amount of time (in seconds)
        that the caller should wait before making the request.

        Returns
        -------
        float
            Seconds to sleep before the next request.  Zero if no wait is
            required.
        """
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call
            sleep_time = max(0.0, self._wait_time - elapsed)
            # Update the timestamp to the moment the request will be made
            self._last_call = now + sleep_time
            return sleep_time

    def update(self, headers: Dict[str, Any], *, default: float) -> None:
        """
        Update the internal wait time based on HTTP response headers.

        Parameters
        ----------
        headers : dict
            HTTP response headers.
        default : float
            Default wait time to use if no relevant header is found.
        """
        new_wait = None

        # Prefer `Retry-After` header if present
        retry_after = headers.get("Retry-After")
        if retry_after is not None:
            try:
                new_wait = float(retry_after)
            except (TypeError, ValueError):
                new_wait = None

        # Fallback to `X-RateLimit-Reset` if present and `Retry-After` was not usable
        if new_wait is None:
            reset = headers.get("X-RateLimit-Reset")
            if reset is not None:
                try:
                    # If the header is an epoch timestamp, compute the delta
                    reset_ts = float(reset)
                    now_ts = time.time()
                    new_wait = max(0.0, reset_ts - now_ts)
                except (TypeError, ValueError):
                    new_wait = None

        # If still no valid header, use the provided default
        if new_wait is None:
            new_wait = float(default)

        # Clamp the wait time to the configured bounds
        new_wait = max(self.min_wait, min(self.max_wait, new_wait))

        with self._lock:
            self._wait_time = new_wait
