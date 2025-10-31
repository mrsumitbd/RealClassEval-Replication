
class RateLimitsInfo:
    def __init__(self, limit, remaining, reset):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def __str__(self):
        return f"RateLimitsInfo(limit={self.limit}, remaining={self.remaining}, reset={self.reset})"

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        return cls(data.get('limit'), data.get('remaining'), data.get('reset'))

    @classmethod
    def from_headers(cls, headers):
        limit = int(headers.get('X-RateLimit-Limit', 0))
        remaining = int(headers.get('X-RateLimit-Remaining', 0))
        reset = int(headers.get('X-RateLimit-Reset', 0))
        return cls(limit, remaining, reset)
