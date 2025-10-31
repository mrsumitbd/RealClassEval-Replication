class CharsCorpusReader:

    def __init__(self, fname, begin=None):
        self.fname = fname
        self.begin = begin

    def __iter__(self):
        begin = self.begin
        with open(self.fname) as f:
            for line in f:
                line = list(line)
                if begin:
                    line = [begin] + line
                yield line