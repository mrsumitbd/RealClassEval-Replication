
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class RateLimitsInfo:
    """
    Holds information about API rate limits.

    Attributes
    ----------
    limit : Optional[int]
        The maximum number of requests allowed in the current window.
    remaining : Optional[int]
        The number of requests remaining in the current window.
    reset : Optional[int]
        Unix timestamp (seconds) when the current window resets.
    used : Optional[int]
        The number of requests used in the current window.
    """

    def __init__(
        self,
        limit: Optional[int] = None,
        remaining: Optional[int] = None,
        reset: Optional[int] = None,
        used: Optional[int] = None,
    ) -> None:
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.used = used

    def __str__(self) -> str:
        parts = []
        if self.limit is not None:
            parts.append(f"limit={self.limit}")
        if self.remaining is not None:
            parts.append(f"remaining={self.remaining}")
        if self.reset is not None:
            # Show both raw timestamp and human‑readable form
            ts = datetime.utcfromtimestamp(
                self.reset).strftime("%Y-%m-%d %H:%M:%S UTC")
            parts.append(f"reset={self.reset} ({ts})")
        if self.used is not None:
            parts.append(f"used={self.used}")
        return f"RateLimitsInfo({', '.join(parts)})"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RateLimitsInfo":
        """
        Create an instance from a dictionary that may contain any of the
        following keys: 'limit', 'remaining', 'reset', 'used'.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        def _int_or_none(value: Any) -> Optional[int]:
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        return cls(
            limit=_int_or_none(data.get("limit")),
            remaining=_int_or_none(data.get("remaining")),
            reset=_int_or_none(data.get("reset")),
            used=_int_or_none(data.get("used")),
        )

    @classmethod
    def from_headers(cls, headers: Dict[str, Any]) -> "RateLimitsInfo":
        """
        Create an instance from HTTP headers. Header names are matched
        case‑insensitively. Common header names are:

        - X-RateLimit-Limit
        - X-RateLimit-Remaining
        - X-RateLimit-Reset
        - X-RateLimit-Used
        """
        if not isinstance(headers, dict):
            raise TypeError("headers must be a dict")

        # Normalise header names to lower case for case‑insensitive lookup
        lower_headers = {k.lower(): v for k, v in headers.items()}

        def _int_or_none(key: str) -> Optional[int]:
            val = lower_headers.get(key.lower())
            try:
                return int(val)
            except (TypeError, ValueError):
                return None

        return cls(
            limit=_int_or_none("x-ratelimit-limit"),
            remaining=_int_or_none("x-ratelimit-remaining"),
            reset=_int_or_none("x-ratelimit-reset"),
            used=_int_or_none("x-ratelimit-used"),
        )
