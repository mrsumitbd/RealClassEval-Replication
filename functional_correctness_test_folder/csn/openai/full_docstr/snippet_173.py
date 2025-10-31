class SingleThing:
    '''A container for a single thing.'''

    def __init__(self, thing):
        '''
        Initialize the container.
        thing -- the thing to store
        '''
        self._thing = thing

    def get_thing(self, _=None):
        '''Get the thing at the given index.'''
        return self._thing

    def get_things(self):
        '''Get the list of things.'''
        return [self._thing]

    def get_name(self):
        '''Get the mDNS server name.'''
        # Prefer a 'name' attribute if present, otherwise fall back to string representation
        return getattr(self._thing, 'name', str(self._thing))
