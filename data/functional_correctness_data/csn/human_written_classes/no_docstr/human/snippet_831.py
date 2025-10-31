class Part:

    def __init__(self, start=None, size=None):
        self._start = start
        self._size = size

    @property
    def start(self):
        return self._start

    @property
    def size(self):
        return self._size