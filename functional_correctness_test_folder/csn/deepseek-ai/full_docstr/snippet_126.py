
import math


class LowestCommonAncestorRMQ:
    '''Lowest common ancestor data structure using a reduction to
       range minimum query
    '''

    def __init__(self, graph):
        '''builds the structure from a given tree
        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        '''
        self.n = len(graph)
        self.LOG = math.floor(math.log2(self.n)) + 1
        self.parent = [[-1] * self.n for _ in range(self.LOG)]
        self.depth = [0] * self.n
        self.euler = []
        self.first = [0] * self.n
        self._dfs(graph, 0, -1)
        self._build_sparse_table()

    def _dfs(self, graph, u, p):
        self.first[u] = len(self.euler)
        self.euler.append(u)
        self.parent[0][u] = p
        for v in graph[u]:
            if v != p:
                self.depth[v] = self.depth[u] + 1
                self._dfs(graph, v, u)
                self.euler.append(u)

    def _build_sparse_table(self):
        m = len(self.euler)
        self.k = math.floor(math.log2(m)) + 1
        self.st = [[0] * m for _ in range(self.k)]
        self.st[0] = self.euler.copy()
        for j in range(1, self.k):
            for i in range(m - (1 << j) + 1):
                left = self.st[j-1][i]
                right = self.st[j-1][i + (1 << (j-1))]
                self.st[j][i] = left if self.depth[left] < self.depth[right] else right

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        l, r = self.first[u], self.first[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = math.floor(math.log2(length))
        left = self.st[k][l]
        right = self.st[k][r - (1 << k) + 1]
        return left if self.depth[left] < self.depth[right] else right
