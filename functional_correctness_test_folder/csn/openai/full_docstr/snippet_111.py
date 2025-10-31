
class Connection:
    '''Connection class'''

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def getInstance():
        '''Static access method.'''
        if Connection._instance is None:
            Connection()
        return Connection._instance

    def __init__(self):
        '''Virtually private constructor.'''
        # Ensure __init__ runs only once
        if getattr(self, '_initialized', False):
            return
        # Place any initialization logic here
        self._initialized = True
