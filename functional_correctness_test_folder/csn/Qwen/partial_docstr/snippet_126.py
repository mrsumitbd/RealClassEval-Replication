
class LowestCommonAncestorRMQ:
    '''Lowest common ancestor data structure using a reduction to
       range minimum query
    '''

    def __init__(self, graph):
        '''builds the structure from a given tree
        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        '''
        import math
        n = len(graph)
        self.euler = []
        self.height = [0] * n
        self.first_occurrence = [-1] * n
        self.log = [0] * (n + 1)
        self.sparse_table = [[0] * (math.ceil(math.log2(n)) + 1)
                             for _ in range(n)]

        def dfs(node, h, parent):
            self.height[node] = h
            if self.first_occurrence[node] == -1:
                self.first_occurrence[node] = len(self.euler)
            self.euler.append(node)
            for neighbor in range(n):
                if graph[node][neighbor] == 1 and neighbor != parent:
                    dfs(neighbor, h + 1, node)
                    self.euler.append(node)

        dfs(0, 0, -1)

        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1

        for i in range(n):
            self.sparse_table[i][0] = i

        for j in range(1, self.log[n] + 1):
            for i in range(n - (1 << j) + 1):
                if self.height[self.sparse_table[i][j - 1]] < self.height[self.sparse_table[i + (1 << (j - 1))][j - 1]]:
                    self.sparse_table[i][j] = self.sparse_table[i][j - 1]
                else:
                    self.sparse_table[i][j] = self.sparse_table[i +
                                                                (1 << (j - 1))][j - 1]

    def query(self, u, v):
        left = self.first_occurrence[u]
        right = self.first_occurrence[v]
        if left > right:
            left, right = right, left
        j = self.log[right - left + 1]
        if self.height[self.sparse_table[left][j]] < self.height[self.sparse_table[right - (1 << j) + 1][j]]:
            return self.euler[self.sparse_table[left][j]]
        else:
            return self.euler[self.sparse_table[right - (1 << j) + 1][j]]
