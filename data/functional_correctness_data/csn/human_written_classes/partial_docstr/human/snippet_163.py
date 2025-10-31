class DateData:
    """
    Class that represents the parsed data with useful information.
    It can be accessed with square brackets like a dict object.
    """

    def __init__(self, *, date_obj=None, period=None, locale=None):
        self.date_obj = date_obj
        self.period = period
        self.locale = locale

    def __getitem__(self, k):
        if not hasattr(self, k):
            raise KeyError(k)
        return getattr(self, k)

    def __setitem__(self, k, v):
        if not hasattr(self, k):
            raise KeyError(k)
        setattr(self, k, v)

    def __repr__(self):
        properties_text = ', '.join(('{}={}'.format(prop, val.__repr__()) for prop, val in self.__dict__.items()))
        return '{}({})'.format(self.__class__.__name__, properties_text)