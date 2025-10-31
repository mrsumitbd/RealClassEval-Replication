
import os


class NullFile:
    '''A file object that is associated to /dev/null.'''

    def __new__(cls):
        """
        Create a new instance that wraps the system's null device.
        """
        instance = super().__new__(cls)
        # Determine the null device name in a cross‑platform way
        null_path = getattr(os, 'devnull', '/dev/null')
        # Open the null device in binary read/write mode
        instance._file = open(null_path, 'wb+')
        return instance

    def __init__(self):
        '''no-op'''
        pass

    # Delegate attribute access to the underlying file object
    def __getattr__(self, name):
        return getattr(self._file, name)

    # Context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    # Optional: provide a readable representation
    def __repr__(self):
        return f"<NullFile at {hex(id(self))}>"
