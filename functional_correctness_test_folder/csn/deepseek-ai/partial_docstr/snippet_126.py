
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
        self.L = []
        self.H = [-1] * self.n
        self.depth = [0] * self.n
        self._dfs(graph, 0, -1)
        self._build_rmq()

    def _dfs(self, graph, u, parent):
        self.H[u] = len(self.L)
        self.L.append(u)
        for v in graph[u]:
            if v != parent:
                self.depth[v] = self.depth[u] + 1
                self._dfs(graph, v, u)
                self.L.append(u)

    def _build_rmq(self):
        self.log_table = [0] * (len(self.L) + 1)
        for i in range(2, len(self.log_table)):
            self.log_table[i] = self.log_table[i // 2] + 1

        self.rmq = []
        self.rmq.append(self.L.copy())
        max_log = self.log_table[len(self.L)] + 1

        for j in range(1, max_log):
            prev = self.rmq[j - 1]
            current = []
            length = 1 << (j - 1)
            for i in range(len(prev) - length):
                if self.depth[prev[i]] < self.depth[prev[i + length]]:
                    current.append(prev[i])
                else:
                    current.append(prev[i + length])
            self.rmq.append(current)

    def query(self, u, v):
        '''Returns the lowest common ancestor of nodes u and v.
        :complexity: O(1)
        '''
        l = self.H[u]
        r = self.H[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = self.log_table[length]
        left = self.rmq[k][l]
        right = self.rmq[k][r - (1 << k) + 1]
        return left if self.depth[left] < self.depth[right] else right
