
class BufferSegment:

    def __init__(self, data, offset):
        self._data = data
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def __len__(self):
        return len(self._data)

    def tobytes(self):
        '''Obtain bytes copy of this segment.'''
        return bytes(self._data)
