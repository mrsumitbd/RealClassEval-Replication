
class NullFile:
    def __new__(cls):
        return cls

    def __init__(self):
        pass

    def write(self, *args, **kwargs):
        pass

    def read(self, *args, **kwargs):
        pass

    def close(self):
        pass

    def flush(self):
        pass

    def isatty(self):
        return False

    def seek(self, *args, **kwargs):
        pass

    def tell(self):
        return 0

    def truncate(self, *args, **kwargs):
        pass
