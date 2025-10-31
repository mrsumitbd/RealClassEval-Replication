class LITERAL:

    def __init__(self, s):
        self._s = s

    def __str__(self):
        return self._s

    def __repr__(self):
        return f'LITERAL({repr(self._s)})'