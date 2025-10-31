class Connection:
    '''Connection class'''
    __instance = None

    @staticmethod
    def getInstance():
        '''Static access method.'''
        if Connection.__instance is None:
            Connection()
        return Connection.__instance

    def __init__(self):
        '''Virtually private constructor.'''
        if Connection.__instance is not None:
            raise Exception("This class is a singleton!")
        Connection.__instance = self
