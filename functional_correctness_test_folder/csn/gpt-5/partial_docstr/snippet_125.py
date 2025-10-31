class FenwickMin:

    def __init__(self, size):
        self.n = int(size)
        self.bit = [float('inf')] * self.n

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
        res = float('inf')
        i = a
        while i >= 0:
            if self.bit[i] < res:
                res = self.bit[i]
            i = (i & (i + 1)) - 1
        return res

    def update(self, a, val):
        '''
        :param int a: index in t
        :param val: a value
        :modifies: sets t[a] to the minimum of t[a] and val
        '''
        if a < 0 or a >= self.n:
            return
        i = a
        while i < self.n:
            if val < self.bit[i]:
                self.bit[i] = val
            i = i | (i + 1)
