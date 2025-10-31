
import os


class NullFile:
    '''A file object that is associated to /dev/null.'''
    def __new__(cls):
        # Open the platform‑independent null device and return the file object.
        return open(os.devnull, 'w+')

    def __init__(self):
        '''no-op'''
        pass
