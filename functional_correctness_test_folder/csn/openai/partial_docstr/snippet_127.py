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
        self.depth = [0] * self.n
        for i in range(1, self.n):
            self.depth[i] = self.depth[prec[i]] + 1

        # compute maximum power of two needed
        self.LOG = 1
        while (1 << self.LOG) <= self.n:
            self.LOG += 1

        # up[i][k] = 2^k-th ancestor of node i
        self.up = [[0] * self.LOG for _ in range(self.n)]
        for i in range(self.n):
            self.up[i][0] = prec[i]
        for k in range(1, self.LOG):
            for i in range(self.n):
                self.up[i][k] = self.up[self.up[i][k-1]][k-1]

    def query(self, u, v):
        '''returns the lowest common ancestor of nodes u and v'''
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # lift u up to depth of v
        diff = self.depth[u] - self.depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = self.up[u][bit]
            diff >>= 1
            bit += 1
        if u == v:
            return u
        # lift both up together
        for k in range(self.LOG-1, -1, -1):
            if self.up[u][k] != self.up[v][k]:
                u = self.up[u][k]
                v = self.up[v][k]
        return self.up[u][0]
