class SerialPattern:

    def __init__(self, patterns):
        self.patterns = patterns

    def match(self, graph, node):
        all_matches = []
        for i, p in enumerate(self.patterns):
            matches, following = p.match(graph, node)
            if not matches:
                return ([], None)
            all_matches.extend(matches)
            if i < len(self.patterns) - 1:
                node = following
        return (all_matches, following)