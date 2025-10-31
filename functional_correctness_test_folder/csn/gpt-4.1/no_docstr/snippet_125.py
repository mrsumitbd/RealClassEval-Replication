
import math


class FenwickMin:

    def __init__(self, size):
        self.N = size
        self.tree = [math.inf] * (self.N + 1)

    def prefixMin(self, a):
        res = math.inf
        i = a + 1
        while i > 0:
            res = min(res, self.tree[i])
            i -= i & -i
        return res

    def update(self, a, val):
        i = a + 1
        while i <= self.N:
            self.tree[i] = min(self.tree[i], val)
            i += i & -i
