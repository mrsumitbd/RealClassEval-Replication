
class SingleThing:
    '''A container for a single thing.'''

    def __init__(self, thing):
        '''
        Initialize the container.
        thing -- the thing to store
        '''
        self.thing = thing

    def get_thing(self, _=None):
        '''Get the thing at the given index.'''
        return self.thing

    def get_things(self):
        '''Get the list of things.'''
        return [self.thing]

    def get_name(self):
        '''Get the mDNS server name.'''
        return 'SingleThing'
