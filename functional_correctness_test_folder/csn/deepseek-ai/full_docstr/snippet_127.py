
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
        self.max_level = math.floor(math.log2(n)) + 1 if n > 1 else 1
        self.ancestors = [[-1] * n for _ in range(self.max_level)]

        # Initialize first level (2^0 ancestors)
        for node in range(n):
            self.ancestors[0][node] = prec[node]

        # Build ancestors table
        for k in range(1, self.max_level):
            for node in range(n):
                if self.ancestors[k-1][node] != -1:
                    self.ancestors[k][node] = self.ancestors[k -
                                                             1][self.ancestors[k-1][node]]
                else:
                    self.ancestors[k][node] = -1

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        if u == v:
            return u

        # Bring u and v to the same level
        if self._get_depth(u) < self._get_depth(v):
            u, v = v, u
        u = self._lift(u, self._get_depth(u) - self._get_depth(v))

        if u == v:
            return u

        # Binary search for the LCA
        for k in range(self.max_level - 1, -1, -1):
            if self.ancestors[k][u] != -1 and self.ancestors[k][u] != self.ancestors[k][v]:
                u = self.ancestors[k][u]
                v = self.ancestors[k][v]
        return self.ancestors[0][u]

    def _get_depth(self, node):
        '''Helper method to compute the depth of a node
        '''
        depth = 0
        while node != 0 and node != -1:
            node = self.ancestors[0][node]
            depth += 1
        return depth

    def _lift(self, node, steps):
        '''Helper method to lift a node up by a certain number of steps
        '''
        for k in range(self.max_level):
            if steps & (1 << k):
                node = self.ancestors[k][node]
                if node == -1:
                    break
        return node
