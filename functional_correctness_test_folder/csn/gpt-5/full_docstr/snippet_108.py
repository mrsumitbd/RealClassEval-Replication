class Details:
    '''Encapsulates data for single IP address.'''

    def __init__(self, details):
        '''Initialize by settings `details` attribute.'''
        self.details = dict(details) if details is not None else {}

    def __getattr__(self, attr):
        '''Return attribute if it exists in details array, else return error.'''
        try:
            return self.details[attr]
        except KeyError:
            raise AttributeError(
                f"{type(self).__name__} object has no attribute {attr!r}")

    @property
    def all(self):
        '''Return all details as dict.'''
        return self.details.copy()
