class ParallelPattern:

    def __init__(self, patterns):
        self.patterns = patterns

    def match(self, graph, nodes):
        if not nodes:
            return ([], None)
        nodes = nodes if isinstance(nodes, list) else [nodes]
        if len(nodes) == 1:
            nodes = graph.siblings(nodes[0])
        else:
            parents = [graph.incoming(n) for n in nodes]
            matches = [set(p) == set(parents[0]) for p in parents[1:]]
            if not all(matches):
                return ([], None)
        if len(self.patterns) != len(nodes):
            return ([], None)
        patterns = self.patterns.copy()
        nodes = nodes.copy()
        all_matches = []
        end_node = None
        for p in patterns:
            found = False
            for n in nodes:
                matches, following = p.match(graph, n)
                if matches:
                    found = True
                    nodes.remove(n)
                    all_matches.extend(matches)
                    if end_node:
                        if end_node != following:
                            return ([], None)
                    else:
                        end_node = following
                    break
            if not found:
                return ([], None)
        return (all_matches, end_node)