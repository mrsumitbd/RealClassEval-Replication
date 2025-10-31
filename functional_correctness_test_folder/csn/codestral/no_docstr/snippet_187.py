
class NodeFinder:

    def __init__(self, matcher, limit=0):

        self.matcher = matcher
        self.limit = limit
        self.count = 0

    def find(self, node, list):

        if self.limit > 0 and self.count >= self.limit:
            return

        if self.matcher(node):
            list.append(node)
            self.count += 1

        for child in node.children:
            self.find(child, list)
