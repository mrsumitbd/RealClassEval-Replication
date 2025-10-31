
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
        # Ensure name is a string
        if not isinstance(name, str):
            name = str(name)
        # Compute SHA-256 hash of the name
        hash_obj = hashlib.sha256(name.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        # Append the string representation of x
        return f"{hash_hex}{x}"
