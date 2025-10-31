class FenwickNode:
    '''Fenwick Tree node.'''

    def __init__(self, parent, children, index=None):
        '''Fenwick Tree node. Single parent and multiple children.
        :param FenwickNode parent: a parent node
        :param list(FenwickNode) children: a list of children nodes
        :param int index: node label
        '''
        self.parent = parent
        self.children = children if children is not None else []
        self.index = index

    def get_ancestors(self):
        '''Return a list of ancestor nodes from the immediate parent up to the root.'''
        ancestors = []
        node = self.parent
        while node is not None:
            ancestors.append(node)
            node = node.parent
        return ancestors
