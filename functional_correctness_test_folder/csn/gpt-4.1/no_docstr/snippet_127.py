
class LowestCommonAncestorShortcuts:

    def __init__(self, prec):
        '''builds the structure from a given tree
        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(nodes)
        '''
        self.n = len(prec)
        self.LOG = 1
        while (1 << self.LOG) <= self.n:
            self.LOG += 1
        # up[node][k] = 2^k-th ancestor of node
        self.up = [[0] * self.LOG for _ in range(self.n)]
        self.depth = [0] * self.n
        # Build depth and up table
        for v in range(self.n):
            if v == 0:
                self.depth[v] = 0
                self.up[v][0] = 0
            else:
                self.depth[v] = self.depth[prec[v]] + 1
                self.up[v][0] = prec[v]
            for k in range(1, self.LOG):
                self.up[v][k] = self.up[self.up[v][k-1]][k-1]

    def query(self, u, v):
        # Bring u and v to the same depth
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        for k in reversed(range(self.LOG)):
            if self.depth[u] - (1 << k) >= self.depth[v]:
                u = self.up[u][k]
        if u == v:
            return u
        for k in reversed(range(self.LOG)):
            if self.up[u][k] != self.up[v][k]:
                u = self.up[u][k]
                v = self.up[v][k]
        return self.up[u][0]
