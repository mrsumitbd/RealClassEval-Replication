
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
        self.euler = []
        self.depth = []
        self.first = [-1] * self.n
        self._dfs(0, 0, graph, set())
        m = len(self.euler)
        # build segment tree storing indices of euler array with minimal depth
        self.size = 1
        while self.size < m:
            self.size <<= 1
        self.seg = [0] * (2 * self.size)
        # initialize leaves
        for i in range(m):
            self.seg[self.size + i] = i
        for i in range(self.size + m, 2 * self.size):
            self.seg[i] = -1  # invalid
        # build internal nodes
        for i in range(self.size - 1, 0, -1):
            left = self.seg[2 * i]
            right = self.seg[2 * i + 1]
            if left == -1:
                self.seg[i] = right
            elif right == -1:
                self.seg[i] = left
            else:
                self.seg[i] = left if self.depth[left] <= self.depth[right] else right

    def _dfs(self, node, d, graph, visited):
        visited.add(node)
        self.first[node] = len(self.euler)
        self.euler.append(node)
        self.depth.append(d)
        for neigh, val in enumerate(graph[node]):
            if val and neigh not in visited:
                self._dfs(neigh, d + 1, graph, visited)
                self.euler.append(node)
                self.depth.append(d)

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l
        l += self.size
        r += self.size
        best = -1
        while l <= r:
            if l & 1:
                idx = self.seg[l]
                if idx != -1 and (best == -1 or self.depth[idx] < self.depth[best]):
                    best = idx
                l += 1
            if not (r & 1):
                idx = self.seg[r]
                if idx != -1 and (best == -1 or self.depth[idx] < self.depth[best]):
                    best = idx
                r -= 1
            l >>= 1
            r >>= 1
        return self.euler[best]
