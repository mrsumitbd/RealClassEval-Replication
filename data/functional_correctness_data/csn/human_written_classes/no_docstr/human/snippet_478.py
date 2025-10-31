class Sentinel:

    def __init__(self, bool_=True):
        self._bool = bool(bool_)

    def __bool__(self):
        return self._bool