
class WordArray:

    def __init__(self, bytes):
        self.bytes = bytes

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0 or key >= len(self.bytes) // 4:
                raise IndexError("Index out of range")
            return int.from_bytes(self.bytes[key*4:(key+1)*4], 'big')
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self.bytes) // 4)
            return [int.from_bytes(self.bytes[i*4:(i+1)*4], 'big') for i in range(start, stop, step)]
        else:
            raise TypeError("Invalid key type")

    def __len__(self):
        return len(self.bytes) // 4
