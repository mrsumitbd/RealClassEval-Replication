
class Variable:

    def __init__(self, val, _type):
        self.val = val
        self._type = _type

    def __str__(self):
        return f"{self.val} ({self._type})"
