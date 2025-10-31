class LowestCommonAncestorShortcuts:

    def __init__(self, prec):
        '''builds the structure from a given tree
        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(nodes)
        '''
        self.n = len(prec)
        self.depth = [0] * self.n
        for i in range(1, self.n):
            self.depth[i] = self.depth[prec[i]] + 1

        LOG = max(1, self.n.bit_length())
        self.up = [[0] * self.n for _ in range(LOG)]
        for v in range(self.n):
            self.up[0][v] = prec[v]
        for k in range(1, LOG):
            prev = self.up[k - 1]
            curr = self.up[k]
            for v in range(self.n):
                curr[v] = prev[prev[v]]

        self.LOG = LOG

    def query(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        diff = self.depth[u] - self.depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = self.up[k][u]
            diff >>= 1
            k += 1

        if u == v:
            return u

        for k in range(self.LOG - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]

        return self.up[0][u]
