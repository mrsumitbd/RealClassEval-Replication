class classproperty:
    """ Implements a @classproperty decorator analogous to @classmethod.
    Solution from: http://stackoverflow.com/questions/128573/using-property-on-classmethodss
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)