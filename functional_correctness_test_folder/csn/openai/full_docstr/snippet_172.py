class MultipleThings:
    '''A container for multiple things.'''

    def __init__(self, things, name):
        '''
        Initialize the container.
        things -- the things to store
        name -- the mDNS server name
        '''
        self._things = list(things)
        self._name = name

    def get_thing(self, idx):
        '''
        Get the thing at the given index.
        idx -- the index
        '''
        return self._things[idx]

    def get_things(self):
        '''Get the list of things.'''
        return self._things

    def get_name(self):
        '''Get the mDNS server name.'''
        return self._name
