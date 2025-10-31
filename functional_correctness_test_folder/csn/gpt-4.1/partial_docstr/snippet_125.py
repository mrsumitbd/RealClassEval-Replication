
import math


class FenwickMin:

    def __init__(self, size):
        self.N = size
        self.tree = [math.inf] * (self.N + 1)
        self.t = [math.inf] * self.N

    def prefixMin(self, a):
        '''
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        '''
        if a < 0:
            return math.inf
        a = min(a, self.N - 1)
        res = math.inf
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
        if not (0 <= a < self.N):
            return
        if val >= self.t[a]:
            return
        self.t[a] = val
        idx = a + 1
        while idx <= self.N:
            if val < self.tree[idx]:
                self.tree[idx] = val
            else:
                break
            idx += idx & -idx
