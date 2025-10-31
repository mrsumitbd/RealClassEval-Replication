
class BufferSegment:

    def __init__(self, offset, data):
        self._offset = offset
        self._data = data

    @property
    def offset(self):
        return self._offset

    def __len__(self):
        return len(self._data)

    def tobytes(self):
        return self._data
