class CompareData:

    def __init__(self, name, benchmark):
        self.name = name
        self.benchmark = benchmark

    def __repr__(self):
        return '<CompareData name=%r value#=%s>' % (self.name, self.benchmark.get_nvalue())