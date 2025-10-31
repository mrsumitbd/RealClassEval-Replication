
class Variable:

    def __init__(self, val, _type):
        self.val = val
        self._type = _type

    def __str__(self):
        return f"Variable(val={self.val}, type={self._type})"
