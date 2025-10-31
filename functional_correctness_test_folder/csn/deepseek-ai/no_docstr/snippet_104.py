
class BufferSegment:

    @property
    def offset(self):
        return self._offset if hasattr(self, '_offset') else 0

    def __len__(self):
        return len(self._data) if hasattr(self, '_data') else 0

    def tobytes(self):
        return bytes(self._data) if hasattr(self, '_data') else b''
