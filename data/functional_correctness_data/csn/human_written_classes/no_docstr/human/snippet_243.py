class IterableToFileAdapter:

    def __init__(self, iterable, size: int, pre_encode: bool=False):
        self.iterator = iter(iterable)
        self.length = size
        self.pre_encode = pre_encode

    def read(self, size: int=-1):
        if self.pre_encode:
            return next(self.iterator, '').encode('iso-8859-1')
        return next(self.iterator, b'')

    def __len__(self) -> int:
        return self.length