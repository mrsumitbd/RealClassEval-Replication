
class FenwickMin:

    def __init__(self, size):
        self.size = size
        self.tree = [float('inf')] * (self.size + 1)

    def prefixMin(self, a):
        '''
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        '''
        if a < 0:
            return float('inf')
        res = float('inf')
        a += 1  # 1-based indexing
        while a > 0:
            res = min(res, self.tree[a])
            a -= a & -a
        return res

    def update(self, a, val):
        '''
        :param int a: index in t
        :param val: a value
        :modifies: sets t[a] to the minimum of t[a] and val
        '''
        a += 1  # 1-based indexing
        while a <= self.size:
            self.tree[a] = min(self.tree[a], val)
            a += a & -a
