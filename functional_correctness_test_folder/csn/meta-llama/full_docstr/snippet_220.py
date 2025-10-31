
class RateLimitsInfo:
    '''Data for rate limits.'''

    def __init__(self, limit, remaining, reset):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def __str__(self):
        '''Get rate limit information as text.'''
        return f"Rate Limit: {self.limit}, Remaining: {self.remaining}, Resets at: {self.reset}"

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        return cls(data['limit'], data['remaining'], data['reset'])

    @classmethod
    def from_headers(cls, headers):
        '''Create RateLimitsInfo from HTTP headers.'''
        limit = int(headers.get('RateLimit-Limit', 0))
        remaining = int(headers.get('RateLimit-Remaining', 0))
        reset = int(headers.get('RateLimit-Reset', 0))
        return cls(limit, remaining, reset)
