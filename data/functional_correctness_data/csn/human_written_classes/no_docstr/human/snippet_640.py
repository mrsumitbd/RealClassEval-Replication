class IntervalTree:

    def __init__(self):
        self.chroms = {}

    def insert(self, interval, linenum=0, other=None):
        chrom = interval.chrom
        start = interval.start
        end = interval.end
        if interval.chrom in self.chroms:
            self.chroms[chrom] = self.chroms[chrom].insert(start, end, linenum, other)
        else:
            self.chroms[chrom] = IntervalNode(start, end, linenum, other)

    def intersect(self, interval, report_func):
        chrom = interval.chrom
        start = interval.start
        end = interval.end
        if chrom in self.chroms:
            self.chroms[chrom].intersect(start, end, report_func)

    def traverse(self, func):
        for item in self.chroms.values():
            item.traverse(func)