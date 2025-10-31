
class RateLimitsInfo:
    def __init__(self, limit=None, remaining=None, reset=None):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def __str__(self):
        return f"RateLimitsInfo(limit={self.limit}, remaining={self.remaining}, reset={self.reset})"

    @classmethod
    def from_dict(cls, data):
        limit = data.get('limit')
        remaining = data.get('remaining')
        reset = data.get('reset')
        return cls(limit, remaining, reset)

    @classmethod
    def from_headers(cls, headers):
        def get_int(header_name):
            value = headers.get(header_name)
            if value is not None:
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None
            return None

        limit = get_int('X-RateLimit-Limit')
        remaining = get_int('X-RateLimit-Remaining')
        reset = get_int('X-RateLimit-Reset')
        return cls(limit, remaining, reset)
