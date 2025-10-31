from tryalgo.range_minimum_query import RangeMinQuery

class LowestCommonAncestorRMQ:
    """Lowest common ancestor data structure using a reduction to
       range minimum query
    """

    def __init__(self, graph):
        """builds the structure from a given tree

        :param graph: adjacency matrix of a tree
        :complexity: O(n log n), with n = len(graph)
        """
        n = len(graph)
        dfs_trace = []
        self.last = [None] * n
        to_visit = [(0, 0, None)]
        succ = [0] * n
        while to_visit:
            level, node, father = to_visit[-1]
            self.last[node] = len(dfs_trace)
            dfs_trace.append((level, node))
            if succ[node] < len(graph[node]) and graph[node][succ[node]] == father:
                succ[node] += 1
            if succ[node] == len(graph[node]):
                to_visit.pop()
            else:
                neighbor = graph[node][succ[node]]
                succ[node] += 1
                to_visit.append((level + 1, neighbor, node))
        self.rmq = RangeMinQuery(dfs_trace, (float('inf'), None))

    def query(self, u, v):
        """:returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        """
        lu = self.last[u]
        lv = self.last[v]
        if lu > lv:
            lu, lv = (lv, lu)
        return self.rmq.range_min(lu, lv + 1)[1]