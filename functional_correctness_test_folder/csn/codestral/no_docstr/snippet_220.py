
class RateLimitsInfo:

    def __init__(self, limit, remaining, reset):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def __str__(self):
        return f"RateLimitsInfo(limit={self.limit}, remaining={self.remaining}, reset={self.reset})"

    @classmethod
    def from_dict(cls, data):
        return cls(data['limit'], data['remaining'], data['reset'])

    @classmethod
    def from_headers(cls, headers):
        return cls(headers['X-RateLimit-Limit'], headers['X-RateLimit-Remaining'], headers['X-RateLimit-Reset'])
