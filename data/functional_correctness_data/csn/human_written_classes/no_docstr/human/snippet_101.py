import mmap

class FastCorpusReader:

    def __init__(self, fname):
        self.fname = fname
        self.f = open(fname, 'rb')

    def __iter__(self):
        m = mmap.mmap(self.f.fileno(), 0, prot=mmap.PROT_READ)
        data = m.readline()
        while data:
            line = data
            data = m.readline()
            line = line.lower()
            line = line.strip().split()
            yield line