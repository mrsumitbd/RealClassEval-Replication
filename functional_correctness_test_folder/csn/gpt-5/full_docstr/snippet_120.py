class NestedDummyClass:
    '''Nested dummy class for testing method resolution.'''

    def __init__(self, value=None):
        self._prop = value

    def run(self):
        '''Do nothing.'''
        return None

    @property
    def prop(self):
        '''Property.'''
        return self._prop
