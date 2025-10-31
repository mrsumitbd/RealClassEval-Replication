class DummyClass:
    '''Dummy class for testing method resolution.'''

    def __init__(self, prop=None):
        self._prop = prop

    def run(self):
        '''Do nothing.'''
        return None

    @property
    def prop(self):
        '''Property.'''
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value
