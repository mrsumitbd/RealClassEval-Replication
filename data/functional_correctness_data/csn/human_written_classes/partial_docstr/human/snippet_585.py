class CoverQuery:
    """Segment tree to maintain a set of integer intervals
    and permitting to query the size of their union.
    """

    def __init__(self, L):
        """creates a structure, where all possible intervals
        will be included in [0, L - 1].
        """
        assert L != []
        self.N = 1
        while self.N < len(L):
            self.N *= 2
        self.c = [0] * (2 * self.N)
        self.s = [0] * (2 * self.N)
        self.w = [0] * (2 * self.N)
        for i, _ in enumerate(L):
            self.w[self.N + i] = L[i]
        for p in range(self.N - 1, 0, -1):
            self.w[p] = self.w[2 * p] + self.w[2 * p + 1]

    def cover(self):
        """:returns: the size of the union of the stored intervals
        """
        return self.s[1]

    def change(self, i, k, offset):
        """when offset = +1, adds an interval [i, k],
        when offset = -1, removes it
        :complexity: O(log L)
        """
        self._change(1, 0, self.N, i, k, offset)

    def _change(self, p, start, span, i, k, offset):
        if start + span <= i or k <= start:
            return
        if i <= start and start + span <= k:
            self.c[p] += offset
        else:
            self._change(2 * p, start, span // 2, i, k, offset)
            self._change(2 * p + 1, start + span // 2, span // 2, i, k, offset)
        if self.c[p] == 0:
            if p >= self.N:
                self.s[p] = 0
            else:
                self.s[p] = self.s[2 * p] + self.s[2 * p + 1]
        else:
            self.s[p] = self.w[p]