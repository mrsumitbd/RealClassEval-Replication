class FenwickMin:
    '''maintains a tree to allow quick updates and queries
    of a virtual table t
    '''

    def __init__(self, size):
        '''stores a table t and allows updates and queries
        of prefix sums in logarithmic time.
        :param size: length of the table
        '''
        self.n = max(0, int(size))
        self.tree = [float('inf')] * (self.n + 1)  # 1-based fenwick tree
        self.arr = [float('inf')] * self.n        # store current point values

    def prefixMin(self, a):
        '''
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        '''
        if a < 0:
            return float('inf')
        if self.n == 0:
            return float('inf')
        if a >= self.n:
            a = self.n - 1
        i = a + 1
        res = float('inf')
        while i > 0:
            if self.tree[i] < res:
                res = self.tree[i]
            i -= i & -i
        return res

    def update(self, a, val):
        '''
        :param int a: index in t
        :param val: a value
        :modifies: sets t[a] to the minimum of t[a] and val
        '''
        if a < 0 or a >= self.n:
            return
        new_val = val if val < self.arr[a] else self.arr[a]
        if new_val == self.arr[a]:
            return
        self.arr[a] = new_val
        i = a + 1
        while i <= self.n:
            if new_val < self.tree[i]:
                self.tree[i] = new_val
            i += i & -i
