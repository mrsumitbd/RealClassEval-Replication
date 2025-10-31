
class FenwickNode:

    def __init__(self, parent, children, index=None):
        self.parent = parent
        self.children = children if children is not None else []
        self.index = index

    def get_ancestors(self):
        ancestors = []
        current = self.parent
        while current is not None:
            ancestors.append(current)
            current = current.parent
        return ancestors
