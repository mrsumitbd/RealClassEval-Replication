
class NullFile:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NullFile, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # No initialization needed for a null file
        pass

    # File-like methods
    def write(self, *args, **kwargs):
        # Discard all writes
        return 0

    def read(self, *args, **kwargs):
        # Return empty string for any read
        return ''

    def readline(self, *args, **kwargs):
        return ''

    def readlines(self, *args, **kwargs):
        return []

    def close(self):
        # Nothing to close
        pass

    def flush(self):
        # Nothing to flush
        pass

    # Context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Do not suppress exceptions
        return False

    # Iterator support
    def __iter__(self):
        return iter([])
