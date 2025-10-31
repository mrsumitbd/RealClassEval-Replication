
import math


class FenwickMin:
    '''maintains a tree to allow quick updates and queries
    of a virtual table t
    '''

    def __init__(self, size):
        '''stores a table t and allows updates and queries
        of prefix minima in logarithmic time.
        :param size: length of the table
        '''
        self.size = size
        # 1‑indexed Fenwick tree, initialized with +inf
        self.tree = [math.inf] * (size + 1)

    def prefixMin(self, a):
        '''
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        '''
        if a < 0:
            return math.inf
        # clamp to valid range
        a = min(a, self.size - 1)
        idx = a + 1  # convert to 1‑based
        res = math.inf
        while idx > 0:
            res = min(res, self.tree[idx])
            idx -= idx & -idx
        return res

    def update(self, a, val):
        '''
        :param int a: index in t
        :param val: a value
        :modifies: sets t[a] to the minimum of t[a] and val
        '''
        if a < 0 or a >= self.size:
            return
        idx = a + 1  # convert to 1‑based
        while idx <= self.size:
            self.tree[idx] = min(self.tree[idx], val)
            idx += idx & -idx
