class Reader:
    """
    Iterator yielding chrom, position, value.
    Values are zero-based.
    Regions which lack a score are ignored.
    """

    def __init__(self, f):
        self.file = f

    def __iter__(self):
        for chrom, start, end, strand, val in IntervalReader(self.file):
            for pos in range(start, end):
                yield (chrom, pos, val)