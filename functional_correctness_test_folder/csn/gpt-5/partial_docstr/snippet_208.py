import os


class NullFile:
    '''A file object that is associated to /dev/null.'''
    def __new__(cls):
        return open(os.devnull, 'w+b')

    def __init__(self):
        '''no-op'''
        pass
