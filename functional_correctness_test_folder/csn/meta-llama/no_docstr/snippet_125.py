
class FenwickMin:

    def __init__(self, size):
        self.size = size
        self.tree = [float('inf')] * (size + 1)

    def prefixMin(self, a):
        min_val = float('inf')
        while a > 0:
            min_val = min(min_val, self.tree[a])
            a -= a & -a
        return min_val

    def update(self, a, val):
        while a <= self.size:
            self.tree[a] = min(self.tree[a], val)
            a += a & -a
