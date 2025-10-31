from collections import Counter, defaultdict

class position:
    """
    Object with information about position: chr,start,end,strand
    as well, with annotation information throuhg :code:`dbannotation` object
    """

    def __init__(self, idl, chr, start, end, strand):
        self.idl = idl
        self.chr = chr
        self.start = int(start)
        self.end = int(end)
        self.strand = strand
        self.coverage = Counter()
        self.counts = Counter()
        self.db_ann = {}

    def list(self):
        return [e for e in map(str, [self.chr, self.start, self.end, self.idl, self.strand])]

    def add_db(self, db, ndb):
        self.db_ann[db] = ndb