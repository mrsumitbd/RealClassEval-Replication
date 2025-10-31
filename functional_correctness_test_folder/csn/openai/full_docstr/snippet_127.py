
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
        # compute maximum power of two needed
        self.LOG = (self.n-1).bit_length()
        # depth array
        self.depth = [0] * self.n
        # up table: up[v][k] = 2^k-th ancestor of v
        self.up = [[0] * self.LOG for _ in range(self.n)]

        # initialize depth and first ancestor
        for v in range(self.n):
            self.up[v][0] = prec[v]
            if v == 0:
                self.depth[v] = 0
            else:
                self.depth[v] = self.depth[prec[v]] + 1

        # fill the rest of the table
        for k in range(1, self.LOG):
            for v in range(self.n):
                self.up[v][k] = self.up[self.up[v][k-1]][k-1]

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        if u == v:
            return u

        # ensure u is the deeper node
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        # lift u up to depth of v
        diff = self.depth[u] - self.depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = self.up[u][k]
            diff >>= 1
            k += 1

        if u == v:
            return u

        # lift both up together
        for k in range(self.LOG-1, -1, -1):
            if self.up[u][k] != self.up[v][k]:
                u = self.up[u][k]
                v = self.up[v][k]

        # now u and v are children of LCA
        return self.up[u][0]
