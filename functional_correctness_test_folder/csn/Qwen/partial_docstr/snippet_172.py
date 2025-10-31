
class MultipleThings:

    def __init__(self, things, name):
        '''
        Initialize the container.
        things -- the things to store
        name -- the mDNS server name
        '''
        self.things = things
        self.name = name

    def get_thing(self, idx):
        return self.things[idx] if 0 <= idx < len(self.things) else None

    def get_things(self):
        '''Get the list of things.'''
        return self.things

    def get_name(self):
        return self.name
