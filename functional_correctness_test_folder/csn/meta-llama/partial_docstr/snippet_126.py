
import math


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
        self.depth = [0] * n
        self.first_occurrence = [-1] * n
        self.euler_tour = []
        self._preprocess(graph)

    def _preprocess(self, graph):
        self._dfs(graph, 0, -1)
        m = len(self.euler_tour)
        self.rmq = RangeMinimumQuery(
            [(self.euler_tour[i][0], i) for i in range(m)])

    def _dfs(self, graph, node, parent):
        self.first_occurrence[node] = len(self.euler_tour)
        self.euler_tour.append((self.depth[node], node))
        for neighbor in range(self.n):
            if graph[node][neighbor] == 1 and neighbor != parent:
                self.depth[neighbor] = self.depth[node] + 1
                self._dfs(graph, neighbor, node)
                self.euler_tour.append((self.depth[node], node))

    def query(self, u, v):
        '''find lowest common ancestor of u and v
        :complexity: O(log n), with n = len(graph)
        '''
        fu = self.first_occurrence[u]
        fv = self.first_occurrence[v]
        if fu > fv:
            fu, fv = fv, fu
        return self.euler_tour[self.rmq.query(fu, fv + 1)][1]


class RangeMinimumQuery:
    def __init__(self, iterable):
        n = len(iterable)
        logn = int(math.log(n, 2)) + 1
        self.table = [[i for i in range(n)]]
        self.values = [val for val, i in iterable]
        for i in range(1, logn):
            prev = self.table[-1]
            self.table.append([prev[j] if self.values[prev[j]] < self.values[prev[j + (
                1 << i - 1)]] else prev[j + (1 << i - 1)] for j in range(n - (1 << i) + 1)])

    def query(self, start, end):
        i = int(math.log(end - start, 2))
        cand1 = self.table[i][start]
        cand2 = self.table[i][end - (1 << i)]
        if self.values[cand1] < self.values[cand2]:
            return cand1
        else:
            return cand2
