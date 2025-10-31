
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
            raise Exception(
                "This class is a singleton! Use getInstance() to get the instance.")
