class BoolOperand:

    def __init__(self, t):
        self.label = t[0]
        self.value = eval(t[0])

    def __bool__(self) -> bool:
        return self.value

    def __str__(self) -> str:
        return self.label
    __repr__ = __str__