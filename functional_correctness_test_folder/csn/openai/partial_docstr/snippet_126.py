
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
        n = len(graph)
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if graph[u][v]:
                    adj[u].append(v)

        # Euler tour
        self.euler = []
        self.depth = []
        self.first = [-1] * n
        visited = [False] * n

        def dfs(u, d):
            visited[u] = True
            self.first[u] = len(self.euler)
            self.euler.append(u)
            self.depth.append(d)
            for v in adj[u]:
                if not visited[v]:
                    dfs(v, d + 1)
                    self.euler.append(u)
                    self.depth.append(d)

        dfs(0, 0)  # root at 0

        m = len(self.euler)
        # log table
        self.log = [0] * (m + 1)
        for i in range(2, m + 1):
            self.log[i] = self.log[i // 2] + 1

        k = self.log[m] + 1
        # Sparse table of indices into euler array
        self.st = [[0] * m for _ in range(k)]
        for i in range(m):
            self.st[0][i] = i
        for j in range(1, k):
            span = 1 << j
            half = span >> 1
            for i in range(m - span + 1):
                left = self.st[j - 1][i]
                right = self.st[j - 1][i + half]
                self.st[j][i] = left if self.depth[left] <= self.depth[right] else right

    def query(self, u, v):
        '''returns the lowest common ancestor of nodes u and v'''
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = self.log[length]
        left = self.st[k][l]
        right = self.st[k][r - (1 << k) + 1]
        idx = left if self.depth[left] <= self.depth[right] else right
        return self.euler[idx]
