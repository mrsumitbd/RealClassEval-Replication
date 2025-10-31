
class FenwickNode:

    def __init__(self, parent, children, index=None):
        self.parent = parent
        self.children = children if children is not None else []
        self.index = index

    def get_ancestors(self):
        ancestors = []
        node = self.parent
        while node is not None:
            ancestors.append(node)
            node = node.parent
        return ancestors
