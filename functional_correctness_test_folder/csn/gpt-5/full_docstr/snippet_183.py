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
        if isinstance(name, str):
            data = name.encode('utf-8')
        elif isinstance(name, (bytes, bytearray, memoryview)):
            data = bytes(name)
        else:
            raise TypeError("name must be str or bytes-like")

        digest = hashlib.md5(data).hexdigest()
        return f"{digest}{x}"
