
class NullFile:
    '''A file object that is associated to /dev/null.'''

    def __new__(cls):
        '''
        Pass through.
        '''
        return super().__new__(cls)

    def __init__(self):
        '''no-op'''
        pass

    def write(self, s):
        pass

    def read(self, size=-1):
        return ''

    def close(self):
        pass

    def flush(self):
        pass

    def seek(self, offset, whence=0):
        pass

    def tell(self):
        return 0

    def truncate(self, size=None):
        pass
