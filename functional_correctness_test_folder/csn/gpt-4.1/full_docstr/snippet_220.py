
class RateLimitsInfo:
    '''Data for rate limits.'''

    def __init__(self, limit=None, remaining=None, reset=None):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def __str__(self):
        '''Get rate limit information as text.'''
        return f"RateLimitsInfo(limit={self.limit}, remaining={self.remaining}, reset={self.reset})"

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        limit = data.get('limit')
        remaining = data.get('remaining')
        reset = data.get('reset')
        return cls(limit, remaining, reset)

    @classmethod
    def from_headers(cls, headers):
        '''Create RateLimitsInfo from HTTP headers.'''
        # Try common header names, case-insensitive
        def get_header(key):
            for k in headers:
                if k.lower() == key.lower():
                    return headers[k]
            return None

        limit = get_header('X-RateLimit-Limit')
        remaining = get_header('X-RateLimit-Remaining')
        reset = get_header('X-RateLimit-Reset')

        # Convert to int if possible
        def to_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return None

        return cls(
            to_int(limit),
            to_int(remaining),
            to_int(reset)
        )
