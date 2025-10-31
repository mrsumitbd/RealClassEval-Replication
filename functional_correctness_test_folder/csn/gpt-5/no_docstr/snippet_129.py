class FenwickNode:

    def __init__(self, parent, children, index=None):
        self.parent = parent
        self.children = list(children) if children is not None else []
        self.index = index

        # Ensure bidirectional linkage with parent
        if self.parent is not None:
            if not hasattr(self.parent, "children") or self.parent.children is None:
                self.parent.children = []
            if self not in self.parent.children:
                self.parent.children.append(self)

        # Ensure children's parent points to this node
        for child in self.children:
            if child is not None:
                child.parent = self

    def get_ancestors(self):
        ancestors = []
        node = self.parent
        while node is not None:
            ancestors.append(node)
            node = node.parent
        return ancestors
