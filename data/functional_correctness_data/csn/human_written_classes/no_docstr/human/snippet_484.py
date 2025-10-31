class UnseekableYetTellable:

    def __init__(self, fh):
        self.fh = fh
        self.offset = 0

    def tell(self):
        return self.offset

    def read(self, size=-1):
        result = self.fh.read(size)
        self.offset += len(result)
        return result