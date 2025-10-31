
class LowestCommonAncestorRMQ:

    def __init__(self, graph):
        '''builds the structure from a given tree
        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        '''
        n = len(graph)
        self.n = n
        self.euler = []
        self.depth = []
        self.first = [-1] * n

        def dfs(u, d, parent):
            self.first[u] = len(self.euler)
            self.euler.append(u)
            self.depth.append(d)
            for v in range(n):
                if graph[u][v] and v != parent:
                    dfs(v, d + 1, u)
                    self.euler.append(u)
                    self.depth.append(d)

        dfs(0, 0, -1)

        m = len(self.depth)
        self.log = [0] * (m + 1)
        for i in range(2, m + 1):
            self.log[i] = self.log[i // 2] + 1

        k = self.log[m] + 1
        self.st = [[0] * m for _ in range(k)]
        for i in range(m):
            self.st[0][i] = i
        for j in range(1, k):
            for i in range(m - (1 << j) + 1):
                l = self.st[j - 1][i]
                r = self.st[j - 1][i + (1 << (j - 1))]
                if self.depth[l] < self.depth[r]:
                    self.st[j][i] = l
                else:
                    self.st[j][i] = r

    def query(self, u, v):
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = self.log[length]
        l_idx = self.st[k][l]
        r_idx = self.st[k][r - (1 << k) + 1]
        if self.depth[l_idx] < self.depth[r_idx]:
            return self.euler[l_idx]
        else:
            return self.euler[r_idx]
