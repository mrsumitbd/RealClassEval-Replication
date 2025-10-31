
class FenwickMin:

    def __init__(self, size):
        self.size = size
        self.tree = [float('inf')] * (size + 1)

    def prefixMin(self, a):
        result = float('inf')
        while a > 0:
            result = min(result, self.tree[a])
            a -= a & -a
        return result

    def update(self, a, val):
        while a <= self.size:
            self.tree[a] = min(self.tree[a], val)
            a += a & -a
