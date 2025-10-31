class Details:
    '''Encapsulates data for single IP address.'''

    def __init__(self, details):
        if details is None:
            details = {}
        elif not isinstance(details, dict):
            try:
                details = dict(details)
            except Exception as e:
                raise TypeError(
                    "details must be a mapping or convertible to dict") from e
        self._details = details

    def __getattr__(self, attr):
        '''Return attribute if it exists in details array, else return error.'''
        try:
            return self._details[attr]
        except KeyError:
            raise AttributeError(f"'Details' object has no attribute '{attr}'")

    @property
    def all(self):
        '''Return all details as dict.'''
        return dict(self._details)
