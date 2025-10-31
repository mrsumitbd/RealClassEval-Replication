
import math


class LowestCommonAncestorRMQ:

    def __init__(self, graph):
        '''builds the structure from a given tree
        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        '''
        self.n = len(graph)
        self.graph = graph
        self.parent = [-1] * self.n
        self.first_visit = [-1] * self.n
        self.euler_tour = []
        self.depth = []
        self.log_n = int(math.log2(self.n)) + 1
        self.rmq = [[float('inf')] * (2 * self.n) for _ in range(self.log_n)]

        self.dfs(0, 0)
        for i in range(len(self.euler_tour)):
            self.rmq[0][i] = self.euler_tour[i]
        for k in range(1, self.log_n):
            for i in range(len(self.euler_tour) - (1 << k) + 1):
                self.rmq[k][i] = min(self.rmq[k - 1][i],
                                     self.rmq[k - 1][i + (1 << (k - 1))])

    def dfs(self, node, depth):
        self.first_visit[node] = len(self.euler_tour)
        self.euler_tour.append(node)
        self.depth.append(depth)
        for neighbor, edge in enumerate(self.graph[node]):
            if edge == 1 and neighbor != self.parent[node]:
                self.parent[neighbor] = node
                self.dfs(neighbor, depth + 1)
                self.euler_tour.append(node)
                self.depth.append(depth)

    def query(self, u, v):
        '''returns the lowest common ancestor of nodes u and v
        :complexity: O(log n), with n = len(graph)
        '''
        u_first_visit = self.first_visit[u]
        v_first_visit = self.first_visit[v]
        if u_first_visit > v_first_visit:
            u_first_visit, v_first_visit = v_first_visit, u_first_visit
        k = int(math.log2(v_first_visit - u_first_visit + 1))
        lca = min(self.rmq[k][u_first_visit], self.rmq[k]
                  [v_first_visit - (1 << k) + 1])
        return lca
