
import math


class FenwickMin:
    def __init__(self, size):
        """
        Create a Fenwick tree that supports prefix minimum queries.
        :param int size: number of elements in the underlying array.
        """
        self.n = size
        # 1‑indexed internal array, initialized with +∞
        self.t = [math.inf] * (self.n + 1)

    def prefixMin(self, a):
        """
        Return the minimum value in the range [0, a] (inclusive).
        If a is negative, return +∞.
        :param int a: index in the original array (0‑based).
        :returns: minimum value in the prefix.
        """
        if a < 0:
            return math.inf
        idx = a + 1  # convert to 1‑based index
        res = math.inf
        while idx > 0:
            res = min(res, self.t[idx])
            idx -= idx & -idx
        return res

    def update(self, a, val):
        """
        Update the element at index a to be the minimum of its current
        value and val. This propagates the change to all relevant
        Fenwick tree nodes.
        :param int a: index in the original array (0‑based).
        :param val: value to compare with the current element.
        """
        idx = a + 1  # convert to 1‑based index
        while idx <= self.n:
            self.t[idx] = min(self.t[idx], val)
            idx += idx & -idx
