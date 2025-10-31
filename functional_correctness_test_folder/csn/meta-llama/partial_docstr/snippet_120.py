
class NestedDummyClass:

    def __init__(self):
        self._prop = None

    def run(self):
        '''Do nothing.'''
        pass

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value
