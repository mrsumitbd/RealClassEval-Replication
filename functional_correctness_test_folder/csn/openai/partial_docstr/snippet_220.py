
class RateLimitsInfo:
    """
    Represents rate‑limit information extracted from a dictionary or HTTP headers.
    """

    def __init__(self, limit=None, remaining=None, reset=None, used=None):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.used = used

    def __str__(self):
        parts = []
        if self.limit is not None:
            parts.append(f"Limit: {self.limit}")
        if self.remaining is not None:
            parts.append(f"Remaining: {self.remaining}")
        if self.reset is not None:
            parts.append(f"Reset: {self.reset}")
        if self.used is not None:
            parts.append(f"Used: {self.used}")
        return ", ".join(parts) if parts else "RateLimitsInfo()"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(limit={self.limit!r}, "
            f"remaining={self.remaining!r}, reset={self.reset!r}, used={self.used!r})"
        )

    @classmethod
    def from_dict(cls, data):
        """Create RateLimitsInfo from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        return cls(
            limit=data.get("limit"),
            remaining=data.get("remaining"),
            reset=data.get("reset"),
            used=data.get("used"),
        )

    @classmethod
    def from_headers(cls, headers):
        """Create RateLimitsInfo from HTTP headers."""
        if not isinstance(headers, dict):
            raise TypeError("headers must be a dict")

        # Normalise header keys to lower case for case‑insensitive lookup
        hdr = {k.lower(): v for k, v in headers.items()}

        def _to_int(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return value

        return cls(
            limit=_to_int(hdr.get("x-ratelimit-limit")),
            remaining=_to_int(hdr.get("x-ratelimit-remaining")),
            reset=_to_int(hdr.get("x-ratelimit-reset")),
            used=_to_int(hdr.get("x-ratelimit-used")),
        )
