
class DummyClass:

    def __init__(self):
        self._prop = None

    def run(self):
        '''Do nothing.'''
        pass

    @property
    def prop(self):
        '''Property.'''
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value
