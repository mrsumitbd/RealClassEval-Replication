class SeqReaderIter:

    def __init__(self, reader):
        self.reader = reader

    def __iter__(self):
        return self

    def __next__(self):
        v = next(self.reader)
        if not v:
            raise StopIteration
        return v