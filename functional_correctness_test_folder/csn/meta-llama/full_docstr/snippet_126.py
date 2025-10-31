
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
        self.root = 0  # assuming 0 is the root
        self.Euler = []  # Euler tour
        self.F = [0] * n  # first occurrence in Euler tour
        self.depth = [0] * n  # depth of each node
        self.logn = int(math.log(n, 2)) + 1
        self.RMQ = [[0] * (2 * n) for _ in range(self.logn)]

        self._preprocess(graph, self.root)

    def _preprocess(self, graph, root):
        self._euler_tour(graph, root, 0)
        for i in range(len(self.Euler)):
            self.RMQ[0][i] = self.Euler[i][1]
        for k in range(1, self.logn):
            for i in range(len(self.Euler) - (1 << k)):
                self.RMQ[k][i] = min(self.RMQ[k - 1][i],
                                     self.RMQ[k - 1][i + (1 << (k - 1))])

    def _euler_tour(self, graph, node, depth):
        self.F[node] = len(self.Euler)
        self.Euler.append((node, depth))
        self.depth[node] = depth
        for neighbor in range(self.n):
            if graph[node][neighbor] == 1:
                self._euler_tour(graph, neighbor, depth + 1)
                self.Euler.append((node, depth))

    def query(self, u, v):
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        fu, fv = self.F[u], self.F[v]
        if fu > fv:
            fu, fv = fv, fu
        length = fv - fu + 1
        k = int(math.log(length, 2))
        min_depth = min(self.RMQ[k][fu], self.RMQ[k][fv - (1 << k) + 1])
        return self.Euler[fu + self.RMQ[k][fu:fv - (1 << k) + 2].index(min_depth)][0]


# Example usage
if __name__ == "__main__":
    graph = [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    lca = LowestCommonAncestorRMQ(graph)
    print(lca.query(4, 6))  # Output: 1
