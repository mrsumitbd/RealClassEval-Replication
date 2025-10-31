
class BufferWithSegmentsCollection:

    def __len__(self):
        return 0

    def __getitem__(self, i):
        raise IndexError("Index out of range")
