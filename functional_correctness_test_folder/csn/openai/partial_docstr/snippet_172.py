class MultipleThings:

    def __init__(self, things, name):
        '''
        Initialize the container.
        things -- the things to store
        name -- the mDNS server name
        '''
        self._things = list(things) if things is not None else []
        self._name = name

    def get_thing(self, idx):
        return self._things[idx]

    def get_things(self):
        '''Get the list of things.'''
        return self._things

    def get_name(self):
        return self._name
