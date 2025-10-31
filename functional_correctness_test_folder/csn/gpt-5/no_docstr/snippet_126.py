class LowestCommonAncestorRMQ:

    def __init__(self, graph):
        '''builds the structure from a given tree
        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        '''
        n = len(graph)
        # Build adjacency list from adjacency matrix
        adj = [[] for _ in range(n)]
        for i in range(n):
            row = graph[i]
            for j in range(n):
                if row[j]:
                    adj[i].append(j)

        # Euler tour + depths + first occurrence
        self.euler = []
        self.depth = []
        self.first = [-1] * n

        def dfs(u, p, d):
            self.first[u] = len(self.euler)
            self.euler.append(u)
            self.depth.append(d)
            for v in adj[u]:
                if v == p:
                    continue
                dfs(v, u, d + 1)
                self.euler.append(u)
                self.depth.append(d)

        # Root at 0
        if n > 0:
            dfs(0, -1, 0)

        m = len(self.euler)
        if m == 0:
            # Empty graph safety
            self.log = [0]
            self.st = [[0]]
            return

        # Precompute logs
        self.log = [0] * (m + 1)
        for i in range(2, m + 1):
            self.log[i] = self.log[i // 2] + 1

        # Build sparse table on depth indices
        K = self.log[m] + 1
        self.st = [[0] * m for _ in range(K)]
        for i in range(m):
            self.st[0][i] = i
        k = 1
        while k < K:
            length = 1 << k
            half = length >> 1
            last_start = m - length
            for i in range(0, last_start + 1):
                a = self.st[k - 1][i]
                b = self.st[k - 1][i + half]
                self.st[k][i] = a if self.depth[a] <= self.depth[b] else b
            k += 1

    def query(self, u, v):
        if u == v:
            return u
        i = self.first[u]
        j = self.first[v]
        if i > j:
            i, j = j, i
        length = j - i + 1
        k = self.log[length]
        a = self.st[k][i]
        b = self.st[k][j - (1 << k) + 1]
        idx = a if self.depth[a] <= self.depth[b] else b
        return self.euler[idx]
