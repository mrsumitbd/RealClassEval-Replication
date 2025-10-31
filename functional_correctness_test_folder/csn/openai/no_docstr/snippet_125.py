
class FenwickMin:
    def __init__(self, size):
        self.n = size
        self.tree = [float('inf')] * (self.n + 1)

    def prefixMin(self, a):
        """Return the minimum value in the range [1, a]."""
        res = float('inf')
        i = a
        while i > 0:
            res = min(res, self.tree[i])
            i -= i & -i
        return res

    def update(self, a, val):
        """Set position a to val and update the tree for decreasing values."""
        i = a
        while i <= self.n:
            self.tree[i] = min(self.tree[i], val)
            i += i & -i
