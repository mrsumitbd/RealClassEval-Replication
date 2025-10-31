
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
        n = len(prec)
        if n == 0:
            return
        self.n = n
        self.max_level = math.floor(math.log2(n)) + 1 if n > 1 else 1
        self.up = [[-1] * n for _ in range(self.max_level)]

        # Initialize the first level (2^0 = 1)
        for v in range(n):
            self.up[0][v] = prec[v]

        # Fill the up table for higher levels
        for k in range(1, self.max_level):
            for v in range(n):
                if self.up[k-1][v] != -1:
                    self.up[k][v] = self.up[k-1][self.up[k-1][v]]
                else:
                    self.up[k][v] = -1

    def query(self, u, v):
        '''Finds the lowest common ancestor of nodes u and v
        :param u: first node
        :param v: second node
        :return: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        # Ensure u is deeper than v
        if u == v:
            return u

        # Bring u and v to the same level
        for k in range(self.max_level - 1, -1, -1):
            if self.up[k][u] != -1 and self.up[k][v] != -1 and self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]

        # Now u and v are at the same level, their parent is the LCA
        return self.up[0][u]
