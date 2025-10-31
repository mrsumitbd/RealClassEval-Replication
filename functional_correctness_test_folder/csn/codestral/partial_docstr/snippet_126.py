
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
        self.log_table = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log_table[i] = self.log_table[i // 2] + 1

        self.euler_tour = []
        self.first_occurrence = [-1] * self.n
        self.depth = [0] * self.n
        self._dfs(graph, 0, -1, 0)

        self.m = len(self.euler_tour)
        self.st = [[0] * self.m for _ in range(self.log_table[self.m] + 1)]
        for i in range(self.m):
            self.st[0][i] = self.euler_tour[i]

        for j in range(1, self.log_table[self.m] + 1):
            for i in range(self.m - (1 << j) + 1):
                self.st[j][i] = min(self.st[j - 1][i], self.st[j - 1]
                                    [i + (1 << (j - 1))], key=lambda x: self.depth[x])

    def _dfs(self, graph, u, parent, current_depth):
        self.first_occurrence[u] = len(self.euler_tour)
        self.euler_tour.append(u)
        self.depth[u] = current_depth
        for v in graph[u]:
            if v != parent:
                self._dfs(graph, v, u, current_depth + 1)
                self.euler_tour.append(u)

    def query(self, u, v):
        l = self.first_occurrence[u]
        r = self.first_occurrence[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = self.log_table[length]
        return min(self.st[k][l], self.st[k][r - (1 << k) + 1], key=lambda x: self.depth[x])
