class Connection:
    '''Connection class'''
    _instance = None

    @staticmethod
    def getInstance():
        if Connection._instance is None:
            Connection._instance = Connection()
        return Connection._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self.connected = False
        self.params = {}
        self._initialized = True
