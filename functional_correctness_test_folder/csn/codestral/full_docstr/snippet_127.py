
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
        self.logn = self.n.bit_length()
        self.prec = prec
        self.shortcuts = [[-1] * self.n for _ in range(self.logn)]
        for i in range(self.n):
            self.shortcuts[0][i] = prec[i]
        for j in range(1, self.logn):
            for i in range(self.n):
                if self.shortcuts[j-1][i] != -1:
                    self.shortcuts[j][i] = self.shortcuts[j -
                                                          1][self.shortcuts[j-1][i]]

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        if u == v:
            return u
        if u > v:
            u, v = v, u
        for j in range(self.logn-1, -1, -1):
            if v - (1 << j) >= u:
                v = self.shortcuts[j][v]
        if u == v:
            return u
        for j in range(self.logn-1, -1, -1):
            if self.shortcuts[j][u] != -1 and self.shortcuts[j][u] != self.shortcuts[j][v]:
                u = self.shortcuts[j][u]
                v = self.shortcuts[j][v]
        return self.prec[u]
