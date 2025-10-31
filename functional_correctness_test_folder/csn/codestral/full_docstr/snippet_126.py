
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
        self.log_n = self.log_table[self.n] + 1
        self.euler_tour = []
        self.first_occurrence = [0] * self.n
        self.depth = [0] * self.n
        self.visited = [False] * self.n
        self._dfs(graph, 0, 0)
        self.m = len(self.euler_tour)
        self.st = [[0] * self.m for _ in range(self.log_n)]
        self.st[0] = self.euler_tour.copy()
        for i in range(1, self.log_n):
            for j in range(self.m - (1 << i) + 1):
                self.st[i][j] = min(self.st[i - 1][j], self.st[i - 1]
                                    [j + (1 << (i - 1))], key=lambda x: self.depth[x])

    def _dfs(self, graph, u, d):
        self.visited[u] = True
        self.first_occurrence[u] = len(self.euler_tour)
        self.euler_tour.append(u)
        self.depth[u] = d
        for v in graph[u]:
            if not self.visited[v]:
                self._dfs(graph, v, d + 1)
                self.euler_tour.append(u)

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        l = self.first_occurrence[u]
        r = self.first_occurrence[v]
        if l > r:
            l, r = r, l
        k = self.log_table[r - l + 1]
        return min(self.st[k][l], self.st[k][r - (1 << k) + 1], key=lambda x: self.depth[x])
