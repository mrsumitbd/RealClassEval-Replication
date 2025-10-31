
class FenwickMin:
    '''maintains a tree to allow quick updates and queries
    of a virtual table t
    '''

    def __init__(self, size):
        '''stores a table t and allows updates and queries
        of prefix mins in logarithmic time.
        :param size: length of the table
        '''
        self.N = size
        self.tree = [float('inf')] * (self.N + 1)

    def prefixMin(self, a):
        '''
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        '''
        if a < 0:
            return float('inf')
        a = min(a, self.N - 1)
        res = float('inf')
        idx = a + 1
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
        idx = a + 1
        while idx <= self.N:
            self.tree[idx] = min(self.tree[idx], val)
            idx += idx & -idx
