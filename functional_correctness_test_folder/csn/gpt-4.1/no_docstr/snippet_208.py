
class NullFile:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def write(self, *args, **kwargs):
        return 0

    def writelines(self, lines):
        pass

    def read(self, *args, **kwargs):
        return ''

    def readline(self, *args, **kwargs):
        return ''

    def readlines(self, *args, **kwargs):
        return []

    def flush(self):
        pass

    def close(self):
        pass

    def seek(self, *args, **kwargs):
        pass

    def tell(self):
        return 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
