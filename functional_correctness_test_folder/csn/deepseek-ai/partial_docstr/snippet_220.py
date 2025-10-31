
class RateLimitsInfo:

    def __str__(self):
        return f"{self.__class__.__name__}()"

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        return cls()

    @classmethod
    def from_headers(cls, headers):
        return cls()
