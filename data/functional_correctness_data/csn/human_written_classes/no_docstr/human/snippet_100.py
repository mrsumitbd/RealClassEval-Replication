class CorpusReader:

    def __init__(self, fname):
        self.fname = fname

    def __iter__(self):
        for line in file(self.fname):
            line = line.strip().split()
            yield line