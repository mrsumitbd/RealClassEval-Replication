
class FenwickMin:

    def __init__(self, size):
        self.size = size
        self.tree = [float('inf')] * (size + 1)

    def prefixMin(self, a):
        if a < 0:
            return float('inf')
        result = float('inf')
        a += 1
        while a > 0:
            result = min(result, self.tree[a])
            a -= a & -a
        return result

    def update(self, a, val):
        a += 1
        while a <= self.size:
            self.tree[a] = min(self.tree[a], val)
            a += a & -a
