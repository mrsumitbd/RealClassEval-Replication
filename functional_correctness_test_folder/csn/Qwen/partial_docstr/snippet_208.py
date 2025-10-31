
class NullFile:
    '''A file object that is associated to /dev/null.'''
    def __new__(cls):
        return open('/dev/null', 'r+')

    def __init__(self):
        '''no-op'''
        pass
