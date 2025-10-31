
import math


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
        self.ancestor = [
            [None] * self.n for _ in range(int(math.log2(self.n)) + 1)]
        for i in range(self.n):
            self.ancestor[0][i] = prec[i]
        for k in range(1, len(self.ancestor)):
            for i in range(self.n):
                self.ancestor[k][i] = self.ancestor[k -
                                                    1][self.ancestor[k - 1][i]]

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        if u == v:
            return u
        if u > v:
            u, v = v, u
        dist = v.bit_length() - 1
        for k in range(dist, -1, -1):
            if self.ancestor[k][v] > u:
                v = self.ancestor[k][v]
        if u == v:
            return u
        dist = u.bit_length() - 1
        for k in range(dist, -1, -1):
            if self.ancestor[k][u] != self.ancestor[k][v]:
                u = self.ancestor[k][u]
                v = self.ancestor[k][v]
        return self.ancestor[0][u]
