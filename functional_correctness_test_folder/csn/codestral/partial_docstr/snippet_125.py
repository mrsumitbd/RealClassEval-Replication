
class FenwickMin:

    def __init__(self, size):
        self.size = size
        self.tree = [float('inf')] * (self.size + 1)

    def prefixMin(self, a):
        res = float('inf')
        a += 1
        while a >= 1:
            res = min(res, self.tree[a])
            a -= a & -a
        return res

    def update(self, a, val):
        a += 1
        while a <= self.size:
            if self.tree[a] > val:
                self.tree[a] = val
                a += a & -a
