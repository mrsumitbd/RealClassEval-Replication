
class FenwickMin:

    def __init__(self, size):
        self.size = size
        self.tree = [float('inf')] * (self.size + 1)

    def prefixMin(self, a):
        res = float('inf')
        while a > 0:
            res = min(res, self.tree[a])
            a -= a & -a
        return res

    def update(self, a, val):
        while a <= self.size:
            self.tree[a] = min(self.tree[a], val)
            a += a & -a
