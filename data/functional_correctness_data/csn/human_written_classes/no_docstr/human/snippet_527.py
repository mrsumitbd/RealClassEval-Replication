class CtxWrapper:

    def __init__(self, v):
        self.__v = v

    def get(self):
        return self.__v

    def set(self, v):
        self.__v = v