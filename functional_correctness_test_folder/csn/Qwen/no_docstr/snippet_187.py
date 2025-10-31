
class NodeFinder:

    def __init__(self, matcher, limit=0):
        self.matcher = matcher
        self.limit = limit

    def find(self, node, lst):
        results = []
        if self.limit == 0 or len(results) < self.limit:
            if self.matcher(node):
                results.append(node)
            for child in getattr(node, 'children', []):
                results.extend(self.find(child, lst))
                if self.limit > 0 and len(results) >= self.limit:
                    break
        return results
