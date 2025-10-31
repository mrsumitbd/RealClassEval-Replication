
import math


class LowestCommonAncestorShortcuts:
    def __init__(self, prec):
        """
        builds the structure from a given tree
        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(nodes)
        """
        self.n = len(prec)
        self.prec = prec
        # depth array
        self.depth = [0] * self.n
        for i in range(1, self.n):
            self.depth[i] = self.depth[prec[i]] + 1

        # binary lifting table
        self.LOG = math.ceil(math.log2(self.n)) if self.n > 1 else 1
        self.up = [[0] * self.n for _ in range(self.LOG)]
        # level 0
        for i in range(self.n):
            self.up[0][i] = prec[i]
        # higher levels
        for k in range(1, self.LOG):
            up_k = self.up[k]
            up_k_1 = self.up[k-1]
            for i in range(self.n):
                up_k[i] = up_k_1[up_k_1[i]]

    def query(self, u, v):
        """
        returns the lowest common ancestor of nodes u and v
        """
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # lift u up to depth of v
        diff = self.depth[u] - self.depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = self.up[bit][u]
            diff >>= 1
            bit += 1
        if u == v:
            return u
        # lift both up together
        for k in range(self.LOG - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        return self.prec[u]
