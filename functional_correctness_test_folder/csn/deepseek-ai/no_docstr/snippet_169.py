
class Cursor:

    def __init__(self):
        self._data = []
        self._index = 0

    def count(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)
