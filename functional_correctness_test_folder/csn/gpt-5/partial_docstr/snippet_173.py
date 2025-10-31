class SingleThing:
    '''A container for a single thing.'''

    def __init__(self, thing):
        '''
        Initialize the container.
        thing -- the thing to store
        '''
        self._thing = thing

    def get_thing(self, _=None):
        return self._thing

    def get_things(self):
        '''Get the list of things.'''
        return [self._thing]

    def get_name(self):
        '''Get the mDNS server name.'''
        # Prefer common naming/title conventions if available
        if hasattr(self._thing, 'get_title') and callable(getattr(self._thing, 'get_title')):
            return self._thing.get_title()
        if hasattr(self._thing, 'title'):
            return getattr(self._thing, 'title')
        if hasattr(self._thing, 'get_name') and callable(getattr(self._thing, 'get_name')):
            return self._thing.get_name()
        if hasattr(self._thing, 'name'):
            return getattr(self._thing, 'name')
        return type(self._thing).__name__
