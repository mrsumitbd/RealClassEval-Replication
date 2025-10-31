
class WordArray:

    def __init__(self, bytes):
        if not isinstance(bytes, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        if len(bytes) % 4 != 0:
            raise ValueError("Length of bytes must be a multiple of 4")
        self._bytes = bytes

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return [int.from_bytes(self._bytes[i*4:(i+1)*4], 'big') for i in range(start, stop, step)]
        if key < 0:
            key += len(self)
        if key < 0 or key >= len(self):
            raise IndexError("Index out of range")
        start = key * 4
        end = start + 4
        return int.from_bytes(self._bytes[start:end], 'big')

    def __len__(self):
        return len(self._bytes) // 4
