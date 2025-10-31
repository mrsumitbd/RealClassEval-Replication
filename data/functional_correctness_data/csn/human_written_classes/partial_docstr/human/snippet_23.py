class Pool:
    """Collection of (data, offset) pairs sorted by data for quick access."""

    def __init__(self):
        self._pool = []

    def FindOrInsert(self, data, offset):
        do = (data, offset)
        index = _BinarySearch(self._pool, do, lambda a, b: a[0] < b[0])
        if index != -1:
            _, offset = self._pool[index]
            return offset
        self._pool.insert(index, do)
        return None

    def Clear(self):
        self._pool = []

    @property
    def Elements(self):
        return [data for data, _ in self._pool]