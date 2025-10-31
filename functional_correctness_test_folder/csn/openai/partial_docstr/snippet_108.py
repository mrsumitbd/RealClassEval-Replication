
class Details:
    '''Encapsulates data for single IP address.'''

    def __init__(self, details):
        # Store the provided details dictionary
        self._details = dict(details)

    def __getattr__(self, attr):
        '''Return attribute if it exists in details array, else return error.'''
        if attr in self._details:
            return self._details[attr]
        raise AttributeError(f"'Details' object has no attribute '{attr}'")

    @property
    def all(self):
        '''Return all details as dict.'''
        return dict(self._details)
