
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
        from collections import deque

        n = len(graph)
        self.depth = [0] * n
        self.euler = []
        self.first_occurrence = [-1] * n
        self.log = [0] * (n + 1)
        self.sparse_table = []

        # Precompute log values for binary lifting
        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1

        # DFS to build Euler tour and depth array
        def dfs(node, parent, d):
            self.depth[node] = d
            self.euler.append(node)
            if self.first_occurrence[node] == -1:
                self.first_occurrence[node] = len(self.euler) - 1
            for neighbor in range(n):
                if graph[node][neighbor] == 1 and neighbor != parent:
                    dfs(neighbor, node, d + 1)
                    self.euler.append(node)

        dfs(0, -1, 0)

        # Build sparse table for range minimum query
        m = len(self.euler)
        self.sparse_table = [[0] * (self.log[m] + 1) for _ in range(m)]
        for i in range(m):
            self.sparse_table[i][0] = i
        for j in range(1, self.log[m] + 1):
            for i in range(m - (1 << j) + 1):
                if self.depth[self.sparse_table[i][j - 1]] < self.depth[self.sparse_table[i + (1 << (j - 1))][j - 1]]:
                    self.sparse_table[i][j] = self.sparse_table[i][j - 1]
                else:
                    self.sparse_table[i][j] = self.sparse_table[i +
                                                                (1 << (j - 1))][j - 1]

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        left = self.first_occurrence[u]
        right = self.first_occurrence[v]
        if left > right:
            left, right = right, left

        k = self.log[right - left + 1]
        if self.depth[self.sparse_table[left][k]] < self.depth[self.sparse_table[right - (1 << k) + 1][k]]:
            return self.euler[self.sparse_table[left][k]]
        else:
            return self.euler[self.sparse_table[right - (1 << k) + 1][k]]
