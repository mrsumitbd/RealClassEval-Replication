
class FenwickNode:
    '''Fenwick Tree node.'''

    def __init__(self, parent, children, index=None):
        '''Fenwick Tree node. Single parent and multiple children.
        :param FenwickNode parent: a parent node
        :param list(FenwickNode) children: a list of children nodes
        :param int index: node label
        '''
        self.parent = parent
        self.children = children
        self.index = index

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
