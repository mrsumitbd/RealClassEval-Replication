
class Cursor:

    def __init__(self):
        self._data = []
        self._index = 0

    def count(self):
        return len(self._data)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._data):
            result = self._data[self._index]
            self._index += 1
            return result
        else:
            self._index = 0
            raise StopIteration
