
class NullFile:
    '''A file object that is associated to /dev/null.'''
    def __new__(cls):
        import os
        return open(os.devnull, 'w+')

    def __init__(self):
        '''no-op'''
        pass
