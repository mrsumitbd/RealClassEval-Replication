
class FenwickNode:

    def __init__(self, parent=None, children=None, index=None):
        self.parent = parent
        self.children = children if children is not None else []
        self.index = index

    def get_ancestors(self):
        ancestors = []
        current = self
        while current.parent is not None:
            ancestors.append(current.parent)
            current = current.parent
        return ancestors
