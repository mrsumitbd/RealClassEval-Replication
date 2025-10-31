
class RateLimitsInfo:

    def __str__(self):
        return f"RateLimitsInfo({self.__dict__})"

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def from_headers(cls, headers):
        instance = cls()
        rate_limit_headers = {
            'RateLimit-Limit': 'limit',
            'RateLimit-Remaining': 'remaining',
            'RateLimit-Reset': 'reset'
        }
        for header_key, attr_name in rate_limit_headers.items():
            if header_key in headers:
                setattr(instance, attr_name, headers[header_key])
        return instance
