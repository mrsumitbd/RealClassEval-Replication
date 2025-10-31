class FenwickMin:

    def __init__(self, size):
        self.n = size
        self.tree = [float('inf')] * (self.n + 1)

    def prefixMin(self, a):
        res = float('inf')
        i = a
        while i > 0:
            if self.tree[i] < res:
                res = self.tree[i]
            i -= i & -i
        return res

    def update(self, a, val):
        i = a
        while i <= self.n:
            if val < self.tree[i]:
                self.tree[i] = val
            i += i & -i
