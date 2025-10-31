class SeqReader:
    """Iterate over all sequences in a file in order"""

    def __init__(self, file, revcomp=False, name='', gap=None):
        self.file = file
        self.revcomp = revcomp
        self.name = name
        self.gap = gap
        self.seqs_read = 0

    def close(self):
        self.file.close()

    def __iter__(self):
        return SeqReaderIter(self)

    def __next__(self):
        return