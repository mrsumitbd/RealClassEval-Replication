
class RateLimitsInfo:
    '''Data for rate limits.'''

    def __str__(self):
        '''Get rate limit information as text.'''
        return str(self.__dict__)

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        instance = cls()
        instance.__dict__.update(data)
        return instance

    @classmethod
    def from_headers(cls, headers):
        '''Create RateLimitsInfo from HTTP headers.'''
        instance = cls()
        rate_limit_headers = {
            'limit': headers.get('X-RateLimit-Limit'),
            'remaining': headers.get('X-RateLimit-Remaining'),
            'reset': headers.get('X-RateLimit-Reset')
        }
        instance.__dict__.update(rate_limit_headers)
        return instance
