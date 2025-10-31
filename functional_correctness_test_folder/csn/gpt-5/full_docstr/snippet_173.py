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
        if _ is None or _ == 0:
            return self._thing
        raise IndexError("SingleThing only contains a single item at index 0")

    def get_things(self):
        '''Get the list of things.'''
        return [self._thing]

    def get_name(self):
        '''Get the mDNS server name.'''
        thing = self._thing
        if hasattr(thing, "get_name") and callable(getattr(thing, "get_name")):
            return thing.get_name()
        if hasattr(thing, "name"):
            return getattr(thing, "name")
        if isinstance(thing, str):
            return thing
        return str(thing)
