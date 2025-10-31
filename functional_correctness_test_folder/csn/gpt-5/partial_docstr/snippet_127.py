class LowestCommonAncestorShortcuts:
    '''Lowest common ancestor data structure using shortcuts to ancestors
    '''

    def __init__(self, prec):
        '''builds the structure from a given tree
        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(nodes)
        '''
        import math
        self.prec = list(prec)
        self.n = len(self.prec)
        self.depth = [0] * self.n
        for v in range(1, self.n):
            self.depth[v] = self.depth[self.prec[v]] + 1

        self.LOG = max(1, math.ceil(math.log2(self.n + 1)))
        self.up = [[0] * self.n for _ in range(self.LOG)]
        for v in range(self.n):
            self.up[0][v] = self.prec[v]
        for k in range(1, self.LOG):
            up_prev = self.up[k - 1]
            up_curr = self.up[k]
            for v in range(self.n):
                up_curr[v] = up_prev[up_prev[v]]

    def query(self, u, v):
        if u == v:
            return u
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
