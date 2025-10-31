
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
