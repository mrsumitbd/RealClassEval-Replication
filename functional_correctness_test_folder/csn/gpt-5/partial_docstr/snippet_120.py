class NestedDummyClass:
    def __init__(self, value=None):
        self._prop = value

    def run(self):
        '''Do nothing.'''
        return None

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value

    @prop.deleter
    def prop(self):
        self._prop = None

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self._prop!r})"
