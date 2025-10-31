
class NullFile:

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(NullFile, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def write(self, *args, **kwargs):
        pass

    def writelines(self, *args, **kwargs):
        pass

    def read(self, *args, **kwargs):
        return ''

    def readline(self, *args, **kwargs):
        return ''

    def readlines(self, *args, **kwargs):
        return []

    def seek(self, *args, **kwargs):
        pass

    def tell(self, *args, **kwargs):
        return 0

    def close(self, *args, **kwargs):
        pass

    def flush(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __getattr__(self, name):
        return lambda *args, **kwargs: None
