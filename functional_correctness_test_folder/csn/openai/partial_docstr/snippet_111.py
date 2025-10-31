
class Connection:
    '''Connection class'''
    _instance = None

    @staticmethod
    def getInstance():
        if Connection._instance is None:
            Connection._instance = Connection()
        return Connection._instance

    def __init__(self):
        if Connection._instance is not None:
            raise RuntimeError(
                "Use getInstance() to get the singleton instance.")
        # Initialize connection attributes here
        self.connected = True
