
class NodeFinder:

    def __init__(self, matcher, limit=0):
        self.matcher = matcher
        self.limit = limit

    def find(self, node, lst):
        found = []

        def _traverse(n):
            if self.limit and len(found) >= self.limit:
                return
            if self.matcher(n):
                found.append(n)
                if self.limit and len(found) >= self.limit:
                    return
            # Try to iterate children if possible
            children = []
            if isinstance(n, dict):
                children = n.values()
            elif isinstance(n, (list, tuple, set)):
                children = n
            # Recursively search children
            for child in children:
                _traverse(child)
        _traverse(node)
        lst.extend(found)
