class SingleThing:
    '''A container for a single thing.'''

    def __init__(self, thing):
        '''
        Initialize the container.
        thing -- the thing to store
        '''
        self._thing = thing

    def get_thing(self, _=None):
        '''Return the stored thing.'''
        return self._thing

    def get_things(self):
        '''Get the list of things.'''
        return [self._thing]

    def get_name(self):
        '''Get the mDNS server name.'''
        # If the thing itself is a string, return it.
        if isinstance(self._thing, str):
            return self._thing
        # Try to get a 'name' attribute.
        return getattr(self._thing, 'name', None)
