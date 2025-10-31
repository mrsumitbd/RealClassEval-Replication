class FenwickNode:
    """Fenwick Tree node."""
    parent = None
    children = None
    index = None

    def __init__(self, parent, children, index=None):
        """Fenwick Tree node. Single parent and multiple children.

        :param FenwickNode parent: a parent node
        :param list(FenwickNode) children: a list of children nodes
        :param int index: node label
        """
        self.children = children
        self.parent = parent
        self.index = index

    def get_ancestors(self):
        """Returns a list of ancestors of the node. Ordered from the earliest.

        :return: node's ancestors, ordered from most recent
        :rtype: list(FenwickNode)
        """
        node = self
        ancestor_list = []
        while node.parent is not None:
            ancestor_list.append(node.parent)
            node = node.parent
        return ancestor_list