
class LowestCommonAncestorRMQ:

    def __init__(self, graph):
        '''builds the structure from a given tree
        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        '''
        import math
        from collections import deque

        n = len(graph)
        self.depth = [0] * n
        self.parent = [[-1] * int(math.log2(n) + 1) for _ in range(n)]
        self.euler = []
        self.first_occurrence = [-1] * n
        self.log = [0] * (n + 1)

        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1

        def dfs(node, par, d):
            self.parent[node][0] = par
            self.depth[node] = d
            self.euler.append(node)
            if self.first_occurrence[node] == -1:
                self.first_occurrence[node] = len(self.euler) - 1
            for i in range(1, len(self.parent[node])):
                if self.parent[node][i - 1] != -1:
                    self.parent[node][i] = self.parent[self.parent[node]
                                                       [i - 1]][i - 1]
            for neighbor in range(n):
                if graph[node][neighbor] == 1 and neighbor != par:
                    dfs(neighbor, node, d + 1)
                    self.euler.append(node)

        dfs(0, -1, 0)

        m = len(self.euler)
        self.st = [[0] * (self.log[m] + 1) for _ in range(m)]

        for i in range(m):
            self.st[i][0] = self.euler[i]

        for j in range(1, self.log[m] + 1):
            for i in range(m - (1 << j) + 1):
                if self.depth[self.st[i][j - 1]] < self.depth[self.st[i + (1 << (j - 1))][j - 1]]:
                    self.st[i][j] = self.st[i][j - 1]
                else:
                    self.st[i][j] = self.st[i + (1 << (j - 1))][j - 1]

    def query(self, u, v):
        left = self.first_occurrence[u]
        right = self.first_occurrence[v]

        if left > right:
            left, right = right, left

        j = self.log[right - left + 1]

        if self.depth[self.st[left][j]] < self.depth[self.st[right - (1 << j) + 1][j]]:
            return self.st[left][j]
        else:
            return self.st[right - (1 << j) + 1][j]
