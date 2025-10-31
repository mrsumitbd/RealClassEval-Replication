
class LowestCommonAncestorShortcuts:

    def __init__(self, prec):
        '''builds the structure from a given tree
        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(prec)
        '''
        self.n = len(prec)
        self.ancestor = [[-1] * self.n for _ in range(20)]
        for i in range(self.n):
            self.ancestor[0][i] = prec[i]
        for k in range(1, 20):
            for i in range(self.n):
                a = self.ancestor[k - 1][i]
                if a != -1:
                    self.ancestor[k][i] = self.ancestor[k - 1][a]

    def query(self, u, v):
        '''returns the lowest common ancestor of u and v
        :complexity: O(log n), with n = number of nodes
        '''
        if u == v:
            return u
        depth_u = self.get_depth(u)
        depth_v = self.get_depth(v)
        if depth_u > depth_v:
            u, v = v, u
            depth_u, depth_v = depth_v, depth_u
        # -- now u is at most as deep as v
        # -- lift v to same depth as u
        depth_diff = depth_v - depth_u
        for k in range(depth_diff.bit_length()):
            if depth_diff & (1 << k):
                v = self.ancestor[k][v]
        if u == v:
            return u
        # -- now u and v are at the same depth
        # -- lift them together until they differ
        for k in range(19, -1, -1):
            if self.ancestor[k][u] != self.ancestor[k][v]:
                u = self.ancestor[k][u]
                v = self.ancestor[k][v]
        return self.ancestor[0][u]

    def get_depth(self, u):
        '''returns the depth of node u
        :complexity: O(log n), with n = number of nodes
        '''
        depth = 0
        for k in range(20):
            if u == -1:
                break
            depth += (1 << k) if (u & (1 << k)) else 0
            u = self.ancestor[k][u]
        return depth
