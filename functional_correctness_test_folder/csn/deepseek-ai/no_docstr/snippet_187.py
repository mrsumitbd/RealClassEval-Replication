
class NodeFinder:

    def __init__(self, matcher, limit=0):
        self.matcher = matcher
        self.limit = limit

    def find(self, node, list):
        results = []
        for item in list:
            if self.matcher(node, item):
                results.append(item)
                if self.limit > 0 and len(results) >= self.limit:
                    break
        return results
