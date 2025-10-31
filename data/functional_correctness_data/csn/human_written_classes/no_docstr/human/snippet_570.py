class _Node:

    def __init__(self, value=None):
        self.value = value
        self.parent = None
        self.children = None

    def add_child(self, node):
        if self.children is None:
            self.children = []
        node.parent = self
        self.children.append(node)

    def add_leaf(self, node):
        if not self.children:
            self.add_child(node)
            return
        leftmost_child = self.children[0]
        while leftmost_child.children:
            leftmost_child = leftmost_child.children[0]
        leftmost_child.add_child(node)