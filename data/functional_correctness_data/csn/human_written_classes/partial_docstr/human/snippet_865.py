class sympy_safe_key:
    """Replacement for pprint._safe_key to be sympy-safe"""
    __slots__ = ['obj']

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return (str(type(self.obj)), id(self.obj)) < (str(type(other.obj)), id(other.obj))