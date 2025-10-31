
class NullFile:

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(NullFile, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass
