
class FenwickMin:
    '''maintains a tree to allow quick updates and queries
    of a virtual table t
    '''

    def __init__(self, size):
        '''stores a table t and allows updates and queries
        of prefix sums in logarithmic time.
        :param size: length of the table
        '''
        self.size = size
        self.tree = [float('inf')] * (size + 1)

    def prefixMin(self, a):
        '''
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        '''
        if a < 0:
            return float('inf')
        a += 1
        min_val = float('inf')
        while a > 0:
            min_val = min(min_val, self.tree[a])
            a -= a & -a
        return min_val

    def update(self, a, val):
        '''
        :param int a: index in t
        :param val: a value
        :modifies: sets t[a] to the minimum of t[a] and val
        '''
        a += 1
        while a <= self.size:
            self.tree[a] = min(self.tree[a], val)
            a += a & -a
