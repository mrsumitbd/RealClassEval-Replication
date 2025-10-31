class Cursor:

    def __init__(self):
        self._count = 0

    def count(self):
        return self._count

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration
