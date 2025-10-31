class LowestCommonAncestorShortcuts:
    '''Lowest common ancestor data structure using shortcuts to ancestors
    '''

    def __init__(self, prec):
        '''builds the structure from a given tree
        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(nodes)
        '''
        self.n = len(prec)
        self.prec = prec
        self.K = max(1, (self.n - 1).bit_length())
        self.up = [[0] * self.n for _ in range(self.K)]
        self.depth = [0] * self.n

        # base: immediate parent
        for v in range(self.n):
            self.up[0][v] = prec[v]

        # depths
        self.depth[0] = 0
        for v in range(1, self.n):
            self.depth[v] = self.depth[prec[v]] + 1

        # binary lifting table
        for k in range(1, self.K):
            up_prev = self.up[k - 1]
            up_cur = self.up[k]
            for v in range(self.n):
                up_cur[v] = up_prev[up_prev[v]]

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        if u == v:
            return u

        # lift to same depth
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

        # lift both
        for k in range(self.K - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]

        return self.up[0][u]
