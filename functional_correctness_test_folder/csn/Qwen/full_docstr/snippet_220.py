
class RateLimitsInfo:
    '''Data for rate limits.'''

    def __init__(self, limit, remaining, reset_time):
        self.limit = limit
        self.remaining = remaining
        self.reset_time = reset_time

    def __str__(self):
        '''Get rate limit information as text.'''
        return (f"Rate Limits: {self.remaining} out of {self.limit} remaining. "
                f"Resets at {self.reset_time}.")

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        return cls(data.get('limit'), data.get('remaining'), data.get('reset_time'))

    @classmethod
    def from_headers(cls, headers):
        '''Create RateLimitsInfo from HTTP headers.'''
        limit = int(headers.get('X-RateLimit-Limit', 0))
        remaining = int(headers.get('X-RateLimit-Remaining', 0))
        reset_time = int(headers.get('X-RateLimit-Reset', 0))
        return cls(limit, remaining, reset_time)
