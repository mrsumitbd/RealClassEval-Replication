
import math


class LowestCommonAncestorRMQ:

    def __init__(self, graph):
        self.n = len(graph)
        self.log_table = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log_table[i] = self.log_table[i // 2] + 1

        self.euler_tour = []
        self.first_occurrence = [-1] * self.n
        self.depth = [0] * self.n
        self._dfs(graph, 0, -1, 0)

        self.m = len(self.euler_tour)
        self.k_max = self.log_table[self.m] + 1
        self.st = [[0] * self.m for _ in range(self.k_max)]
        self._build_sparse_table()

    def _dfs(self, graph, u, parent, current_depth):
        self.first_occurrence[u] = len(self.euler_tour)
        self.euler_tour.append(u)
        self.depth[u] = current_depth
        for v in graph[u]:
            if v != parent:
                self._dfs(graph, v, u, current_depth + 1)
                self.euler_tour.append(u)

    def _build_sparse_table(self):
        for i in range(self.m):
            self.st[0][i] = i

        for k in range(1, self.k_max):
            for i in range(self.m - (1 << k) + 1):
                left = self.st[k - 1][i]
                right = self.st[k - 1][i + (1 << (k - 1))]
                if self.depth[self.euler_tour[left]] < self.depth[self.euler_tour[right]]:
                    self.st[k][i] = left
                else:
                    self.st[k][i] = right

    def query(self, u, v):
        l = self.first_occurrence[u]
        r = self.first_occurrence[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = self.log_table[length]
        left = self.st[k][l]
        right = self.st[k][r - (1 << k) + 1]
        if self.depth[self.euler_tour[left]] < self.depth[self.euler_tour[right]]:
            return self.euler_tour[left]
        else:
            return self.euler_tour[right]
