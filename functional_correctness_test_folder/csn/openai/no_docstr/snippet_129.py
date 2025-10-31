
class FenwickNode:
    """
    A node used in a Fenwick (Binary Indexed) tree representation.
    Each node keeps a reference to its parent, a list of its children,
    and an optional index that can be used to identify the node.
    """

    def __init__(self, parent, children, index=None):
        """
        Parameters
        ----------
        parent : FenwickNode or None
            Reference to the parent node.  ``None`` indicates that this
            node is the root of the tree.
        children : list[FenwickNode]
            List of child nodes.  The list may be empty for leaf nodes.
        index : int, optional
            An optional identifier for the node.  It is not used by the
            tree logic but can be helpful for debugging or external
            mapping.
        """
        self.parent = parent
        self.children = children
        self.index = index

        # If a parent is supplied, automatically add this node to its
        # children list.  This keeps the tree structure consistent
        # regardless of whether the caller added the node manually.
        if parent is not None and self not in parent.children:
            parent.children.append(self)

    def get_ancestors(self):
        """
        Return a list of ancestor nodes from the root down to the
        immediate parent of this node.

        Returns
        -------
        list[FenwickNode]
            Ordered list of ancestors.  The first element is the root
            node, and the last element is the direct parent of this
            node.  If the node is the root, an empty list is returned.
        """
        ancestors = []
        node = self.parent
        while node is not None:
            ancestors.append(node)
            node = node.parent
        ancestors.reverse()
        return ancestors
