class FenwickMin:
    """maintains a tree to allow quick updates and queries
    of a virtual table t
    """

    def __init__(self, size):
        """stores a table t and allows updates and queries
        of prefix sums in logarithmic time.

        :param size: length of the table
        """
        self.s = [float('+inf')] * (size + 1)

    def prefixMin(self, a):
        """
        :param int a: index in t, negative a will return infinity
        :returns: min(t[0], ... ,t[a])
        """
        i = a + 1
        retval = float('+inf')
        while i > 0:
            retval = min(retval, self.s[i])
            i -= i & -i
        return retval

    def update(self, a, val):
        """
        :param int a: index in t
        :param val: a value
        :modifies: sets t[a] to the minimum of t[a] and val
        """
        i = a + 1
        while i < len(self.s):
            self.s[i] = min(self.s[i], val)
            i += i & -i