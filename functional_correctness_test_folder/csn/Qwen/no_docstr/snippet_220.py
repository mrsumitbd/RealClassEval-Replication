
class RateLimitsInfo:
    def __init__(self, limit, remaining, reset):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def __str__(self):
        return f"RateLimitsInfo(limit={self.limit}, remaining={self.remaining}, reset={self.reset})"

    @classmethod
    def from_dict(cls, data):
        return cls(
            limit=data.get('limit'),
            remaining=data.get('remaining'),
            reset=data.get('reset')
        )

    @classmethod
    def from_headers(cls, headers):
        return cls(
            limit=int(headers.get('X-RateLimit-Limit', 0)),
            remaining=int(headers.get('X-RateLimit-Remaining', 0)),
            reset=int(headers.get('X-RateLimit-Reset', 0))
        )
