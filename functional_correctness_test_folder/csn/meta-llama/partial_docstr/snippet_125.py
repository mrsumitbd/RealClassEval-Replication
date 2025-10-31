
import sys


class FenwickMin:

    def __init__(self, size):
        self.size = size
        self.tree = [sys.maxsize] * (size + 1)

    def prefixMin(self, a):
        '''
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        '''
        if a < 0:
            return sys.maxsize
        min_val = sys.maxsize
        a += 1
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
