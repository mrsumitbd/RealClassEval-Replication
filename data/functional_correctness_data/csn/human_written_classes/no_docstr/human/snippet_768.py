from operator import lt

class Graph:

    def __init__(self, undirected=True):
        self.nodes = set()
        self.edges = {}
        self.cluster_lookup = {}
        self.no_link = {}
        self.undirected = undirected

    def add_edge(self, n1, n2, w):
        self.nodes.add(n1)
        self.nodes.add(n2)
        self.edges.setdefault(n1, {}).update({n2: w})
        if self.undirected:
            self.edges.setdefault(n2, {}).update({n1: w})

    def connected_components(self, threshold=0.9, op=lt):
        if not self.undirected:
            warn = 'Warning, connected _components not '
            warn += 'defined for a directed graph'
            print(warn)
            return None
        else:
            nodes = set(self.nodes)
            components, visited = ([], set())
            while len(nodes) > 0:
                connected, visited = self.dfs(nodes.pop(), visited, threshold, op)
                connected = set(connected)
                for node in connected:
                    if node in nodes:
                        nodes.remove(node)
                subgraph = Graph()
                subgraph.nodes = connected
                subgraph.no_link = self.no_link
                for s in subgraph.nodes:
                    for k, v in list(self.edges.get(s, {}).items()):
                        if k in subgraph.nodes:
                            subgraph.edges.setdefault(s, {}).update({k: v})
                    if s in self.cluster_lookup:
                        subgraph.cluster_lookup[s] = self.cluster_lookup[s]
                components.append(subgraph)
            return components

    def dfs(self, v, visited, threshold, op=lt, first=None):
        aux = [v]
        visited.add(v)
        if first is None:
            first = v
        for i in (n for n, w in list(self.edges.get(v, {}).items()) if op(w, threshold) and n not in visited):
            x, y = self.dfs(i, visited, threshold, op, first)
            aux.extend(x)
            visited = visited.union(y)
        return (aux, visited)