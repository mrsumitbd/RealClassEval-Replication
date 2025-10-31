class BoolNot:

    def __init__(self, t):
        self.arg = t[0][1]

    def __bool__(self) -> bool:
        v = bool(self.arg)
        return not v

    def __str__(self) -> str:
        return '~' + str(self.arg)
    __repr__ = __str__