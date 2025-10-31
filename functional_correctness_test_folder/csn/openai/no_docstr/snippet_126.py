
import math
import sys


class LowestCommonAncestorRMQ:
    def __init__(self, graph):
        """
        builds the structure from a given tree
        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        """
        n = len(graph)
        # build adjacency list
        self.adj = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if graph[i][j]:
                    self.adj[i].append(j)

        # Euler tour
        self.euler = []
        self.depth = []
        self.first = [-1] * n

        sys.setrecursionlimit(max(1000, n * 2))

        def dfs(u, p, d):
            self.first[u] = len(self.euler)
            self.euler.append(u)
            self.depth.append(d)
            for v in self.adj[u]:
                if v == p:
                    continue
                dfs(v, u, d + 1)
                self.euler.append(u)
                self.depth.append(d)

        dfs(0, -1, 0)

        m = len(self.euler)
        # log table
        self.log = [0] * (m + 1)
        for i in range(2, m + 1):
            self.log[i] = self.log[i // 2] + 1

        K = self.log[m] + 1
        # sparse table of indices into euler array
        self.st = [[0] * m for _ in range(K)]
        for i in range(m):
            self.st[0][i] = i
        for k in range(1, K):
            span = 1 << k
            half = span >> 1
            for i in range(m - span + 1):
                left = self.st[k - 1][i]
                right = self.st[k - 1][i + half]
                if self.depth[left] <= self.depth[right]:
                    self.st[k][i] = left
                else:
                    self.st[k][i] = right

    def query(self, u, v):
        """
        returns the lowest common ancestor of nodes u and v
        """
        if u == v:
            return u
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
