
import math


class LowestCommonAncestorRMQ:

    def __init__(self, graph):
        self.n = len(graph)
        self.LOG = math.floor(math.log2(self.n)) + 1
        self.parent = [[-1] * self.n for _ in range(self.LOG)]
        self.depth = [0] * self.n
        self.visited = [False] * self.n
        self._dfs(graph, 0)
        self._precompute_parents()

    def _dfs(self, graph, root):
        stack = [(root, -1, 0)]
        while stack:
            u, p, d = stack.pop()
            if not self.visited[u]:
                self.visited[u] = True
                self.parent[0][u] = p
                self.depth[u] = d
                for v in reversed(graph[u]):
                    if v != p:
                        stack.append((v, u, d + 1))

    def _precompute_parents(self):
        for k in range(1, self.LOG):
            for v in range(self.n):
                if self.parent[k-1][v] != -1:
                    self.parent[k][v] = self.parent[k-1][self.parent[k-1][v]]

    def query(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        for k in range(self.LOG-1, -1, -1):
            if self.depth[u] - (1 << k) >= self.depth[v]:
                u = self.parent[k][u]
        if u == v:
            return u
        for k in range(self.LOG-1, -1, -1):
            if self.parent[k][u] != -1 and self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        return self.parent[0][u]
