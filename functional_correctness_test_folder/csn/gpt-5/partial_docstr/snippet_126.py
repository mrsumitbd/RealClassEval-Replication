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
                if i != j and row[j]:
                    adj[i].append(j)
        self.adj = adj

        if n == 0:
            # Empty structure
            self.euler = []
            self.depths = []
            self.first = []
            self.log = [0]
            self.st = [[]]
            return

        # Euler tour and depths
        euler = []
        depths = []
        first = [-1] * n
        depth = [0] * n

        # Iterative DFS with explicit enter/back actions to build Euler tour
        stack = [('visit', 0, -1)]
        depth[0] = 0
        while stack:
            typ, u, p = stack.pop()
            if typ == 'visit':
                if first[u] == -1:
                    first[u] = len(euler)
                euler.append(u)
                depths.append(depth[u])
                # Push children in reverse order so traversal is in original order
                for v in reversed(adj[u]):
                    if v == p:
                        continue
                    stack.append(('back', u, p))
                    depth[v] = depth[u] + 1
                    stack.append(('visit', v, u))
            else:  # 'back' action
                euler.append(u)
                depths.append(depth[u])

        self.euler = euler
        self.depths = depths
        self.first = first

        m = len(euler)
        # Precompute logs
        log = [0] * (m + 1)
        for i in range(2, m + 1):
            log[i] = log[i // 2] + 1
        self.log = log

        # Build Sparse Table over depths; store indices into euler
        kmax = log[m]
        st = [[0] * m for _ in range(kmax + 1)]
        for i in range(m):
            st[0][i] = i
        j = 1
        while (1 << j) <= m:
            span = 1 << j
            half = span >> 1
            prev = st[j - 1]
            cur = st[j]
            for i in range(m - span + 1):
                left = prev[i]
                right = prev[i + half]
                cur[i] = left if depths[left] <= depths[right] else right
            j += 1
        self.st = st

    def query(self, u, v):
        if self.n == 0:
            return None
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("query nodes out of range")
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = self.log[length]
        i1 = self.st[k][l]
        i2 = self.st[k][r - (1 << k) + 1]
        idx = i1 if self.depths[i1] <= self.depths[i2] else i2
        return self.euler[idx]
