class Connection:
    _instance = None

    @staticmethod
    def getInstance():
        if Connection._instance is None:
            Connection._instance = Connection()
        return Connection._instance

    def __init__(self):
        pass
