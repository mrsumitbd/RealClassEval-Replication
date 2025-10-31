
import time
from typing import Dict, Optional


class SentinelHubRateLimit:
    """
    Simple rate‑limit helper for Sentinel‑Hub requests.

    The class keeps track of the earliest time a new request may be sent.
    After each request the caller should call :meth:`update` with the
    response headers so that the next allowed time can be adjusted
    according to the server’s rate‑limit information.
    """

    def __init__(
        self,
        num_processes: int = 1,
        minimum_wait_time: float = 0.05,
        maximum_wait_time: float = 60.0,
    ):
        """
        :param num_processes: Number of parallel download processes running.
        :param minimum_wait_time: Minimum wait time between two consecutive download requests in seconds.
        :param maximum_wait_time: Maximum wait time between two consecutive download requests in seconds.
        """
        self.num_processes = max(1, int(num_processes))
        self.minimum_wait_time = float(minimum_wait_time)
        self.maximum_wait_time = float(maximum_wait_time)
        # The earliest timestamp (in seconds since epoch) at which a request may be sent.
        self._next_time: float = 0.0

    def register_next(self) -> float:
        """
        Return the number of seconds that must be waited before the next request
        can be sent.  The internal ``_next_time`` is updated to enforce the
        minimum wait time between requests.

        :return: Seconds to wait (0.0 if no wait is required).
        """
        now = time.time()
        wait = max(0.0, self._next_time - now)
        # Schedule the next request after the minimum wait time.
        self._next_time = now + self.minimum_wait_time
        return wait

    def _clamp_wait(self, wait: float) -> float:
        """Clamp the wait time between the configured min/max limits."""
        return max(self.minimum_wait_time, min(self.maximum_wait_time, wait))

    def _parse_retry_after(self, headers: Dict[str, str]) -> Optional[float]:
        """
        Parse the ``Retry-After`` header if present.
        The header may contain either a number of seconds or an HTTP date.
        """
        retry = headers.get("Retry-After")
        if retry is None:
            return None
        retry = retry.strip()
        # Try to interpret as seconds
        try:
            return float(retry)
        except ValueError:
            pass
        # Try to interpret as HTTP date
        try:
            from email.utils import parsedate_to_datetime

            dt = parsedate_to_datetime(retry)
            return max(0.0, (dt - time.time()).total_seconds())
        except Exception:
            return None

    def _parse_rate_limit_reset(self, headers: Dict[str, str]) -> Optional[float]:
        """
        Parse the ``X-RateLimit-Reset`` header if present.
        The header is expected to be an epoch timestamp in seconds.
        """
        reset = headers.get("X-RateLimit-Reset")
        if reset is None:
            return None
        try:
            return float(reset)
        except ValueError:
            return None

    def update(self, headers: Dict[str, str], *, default: float) -> None:
        """
        Update the next possible download time if the service has responded with the rate limit.

        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        """
        now = time.time()
        # 1. Check for Retry-After header
        retry_after = self._parse_retry_after(headers)
        if retry_after is not None:
            wait = retry_after
        else:
            # 2. Check for X-RateLimit-Reset header
            reset_time = self._parse_rate_limit_reset(headers)
            if reset_time is not None:
                wait = max(0.0, reset_time - now)
            else:
                # 3. Fallback to default (milliseconds -> seconds)
                wait = default / 1000.0

        # Clamp the wait time to the configured limits
        wait = self._clamp_wait(wait)

        # Update the next allowed time
        self._next_time = max(self._next_time, now + wait)
