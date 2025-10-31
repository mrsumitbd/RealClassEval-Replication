
import hashlib


class Reader:
    '''
    The reader provides integration with cache.
    @ivar options: An options object.
    @type options: I{Options}
    '''

    def __init__(self, options):
        '''
        @param options: An options object.
        @type options: I{Options}
        '''
        self.options = options

    def mangle(self, name, x):
        '''
        Mangle the name by hashing the I{name} and appending I{x}.
        @return: the mangled name.
        '''
        hashed_name = hashlib.sha256(name.encode()).hexdigest()
        return f"{hashed_name}_{x}"
