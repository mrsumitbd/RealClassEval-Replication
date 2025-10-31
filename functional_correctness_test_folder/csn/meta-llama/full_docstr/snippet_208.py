
import os


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

    def __getattr__(self, name):
        if name in ['fileno', 'close', 'read', 'readline', 'readlines', 'seek', 'tell', 'write', 'writelines', 'flush', 'truncate']:
            return lambda *args, **kwargs: None
        elif name in ['closed', 'isatty', 'mode']:
            return getattr(open(os.devnull, 'r'), name)
        else:
            raise AttributeError(
                f"'NullFile' object has no attribute '{name}'")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"
