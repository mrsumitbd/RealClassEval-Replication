
class RateLimitsInfo:
    '''Data for rate limits.'''

    def __init__(self, limit=None, remaining=None, reset=None, used=None):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        # If used is not explicitly provided, compute it from limit and remaining
        if used is None and limit is not None and remaining is not None:
            try:
                self.used = int(limit) - int(remaining)
            except Exception:
                self.used = None
        else:
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
        return ", ".join(parts) if parts else "<No rate limit data>"

    @classmethod
    def _parse_value(cls, value):
        """Try to convert a value to int, otherwise return None."""
        if value is None:
            return None
        try:
            return int(value)
        except Exception:
            return None

    @classmethod
    def from_dict(cls, data):
        """Create RateLimitsInfo from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        limit = cls._parse_value(data.get("limit"))
        remaining = cls._parse_value(data.get("remaining"))
        reset = cls._parse_value(data.get("reset"))
        used = cls._parse_value(data.get("used"))
        return cls(limit=limit, remaining=remaining, reset=reset, used=used)

    @classmethod
    def from_headers(cls, headers):
        """Create RateLimitsInfo from HTTP headers."""
        if not isinstance(headers, dict):
            raise TypeError("headers must be a dict")
        # Common header names for rate limits
        header_map = {
            "limit": ["X-RateLimit-Limit", "X-RateLimit-Limit", "X-RateLimit-Limit"],
            "remaining": ["X-RateLimit-Remaining", "X-RateLimit-Remaining"],
            "reset": ["X-RateLimit-Reset", "X-RateLimit-Reset"],
            "used": ["X-RateLimit-Used", "X-RateLimit-Used"],
        }

        def get_header(keys):
            for key in keys:
                if key in headers:
                    return headers[key]
            return None

        limit = cls._parse_value(get_header(header_map["limit"]))
        remaining = cls._parse_value(get_header(header_map["remaining"]))
        reset = cls._parse_value(get_header(header_map["reset"]))
        used = cls._parse_value(get_header(header_map["used"]))
        return cls(limit=limit, remaining=remaining, reset=reset, used=used)
