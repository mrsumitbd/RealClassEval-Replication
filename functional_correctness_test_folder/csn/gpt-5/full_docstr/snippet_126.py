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
        self.n = n
        # Build adjacency list from adjacency matrix
        adj = [[] for _ in range(n)]
        for i in range(n):
            row = graph[i]
            for j in range(n):
                if row[j]:
                    adj[i].append(j)
        self._adj = adj

        # Euler tour and depth arrays
        euler = []
        depth = []
        first = [-1] * n

        def dfs(u, p, d):
            first[u] = len(euler)
            euler.append(u)
            depth.append(d)
            for v in adj[u]:
                if v == p:
                    continue
                dfs(v, u, d + 1)
                euler.append(u)
                depth.append(d)

        if n > 0:
            dfs(0, -1, 0)

        self.euler = euler
        self.depth = depth
        self.first = first

        m = len(depth)
        if m == 0:
            # Empty tree edge case
            self.log = [0]
            self.st = [[0]]
            return

        # Precompute logs
        log = [0] * (m + 1)
        for i in range(2, m + 1):
            log[i] = log[i // 2] + 1
        self.log = log

        # Build sparse table storing indices into depth
        K = log[m] + 1
        st = [[0] * m for _ in range(K)]
        for i in range(m):
            st[0][i] = i
        k = 1
        while (1 << k) <= m:
            span = 1 << k
            half = span >> 1
            prev = st[k - 1]
            curr = st[k]
            for i in range(0, m - span + 1):
                a = prev[i]
                b = prev[i + half]
                curr[i] = a if depth[a] <= depth[b] else b
            k += 1
        self.st = st

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        if self.n == 0:
            return None
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l
        k = self.log[r - l + 1]
        a = self.st[k][l]
        b = self.st[k][r - (1 << k) + 1]
        idx = a if self.depth[a] <= self.depth[b] else b
        return self.euler[idx]
