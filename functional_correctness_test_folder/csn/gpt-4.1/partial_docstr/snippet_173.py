
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
        if hasattr(self._thing, 'name'):
            return self._thing.name
        elif hasattr(self._thing, 'get_name') and callable(self._thing.get_name):
            return self._thing.get_name()
        else:
            return str(self._thing)
