class EmplaceIter:

    def __init__(self, it):
        self.it = it
        self.ret = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.ret) > 0:
            v = self.ret.pop()
            return v
        return next(self.it)
    next = __next__

    def put_back(self, v):
        self.ret.append(v)