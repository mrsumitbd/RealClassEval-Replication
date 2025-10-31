class FenwickNode:
    '''Fenwick Tree node.'''

    def __init__(self, parent, children, index=None):
        '''Fenwick Tree node. Single parent and multiple children.
        :param FenwickNode parent: a parent node
        :param list(FenwickNode) children: a list of children nodes
        :param int index: node label
        '''
        self.parent = parent
        self.index = index
        self.children = list(children) if children is not None else []

        # Ensure children's parent is set to self
        for child in self.children:
            if child is not None:
                child.parent = self

        # Ensure this node is registered in parent's children
        if self.parent is not None:
            if self not in self.parent.children:
                self.parent.children.append(self)

    def get_ancestors(self):
        '''Returns a list of ancestors of the node. Ordered from the earliest.
        :return: node's ancestors, ordered from most recent
        :rtype: list(FenwickNode)
        '''
        ancestors = []
        current = self.parent
        while current is not None:
            ancestors.append(current)
            current = current.parent
        return ancestors
