class LowestCommonAncestorShortcuts:
    """Lowest common ancestor data structure using shortcuts to ancestors
    """

    def __init__(self, prec):
        """builds the structure from a given tree

        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(nodes)
        """
        n = len(prec)
        self.level = [None] * n
        self.level[0] = 0
        for u in range(1, n):
            self.level[u] = 1 + self.level[prec[u]]
        depth = log2ceil(max((self.level[u] for u in range(n)))) + 1
        self.anc = [[0] * n for _ in range(depth)]
        for u in range(n):
            self.anc[0][u] = prec[u]
        for k in range(1, depth):
            for u in range(n):
                self.anc[k][u] = self.anc[k - 1][self.anc[k - 1][u]]

    def query(self, u, v):
        """:returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        """
        if self.level[u] > self.level[v]:
            u, v = (v, u)
        depth = len(self.anc)
        for k in range(depth - 1, -1, -1):
            if self.level[u] <= self.level[v] - (1 << k):
                v = self.anc[k][v]
        assert self.level[u] == self.level[v]
        if u == v:
            return u
        for k in range(depth - 1, -1, -1):
            if self.anc[k][u] != self.anc[k][v]:
                u = self.anc[k][u]
                v = self.anc[k][v]
        assert self.anc[0][u] == self.anc[0][v]
        return self.anc[0][u]