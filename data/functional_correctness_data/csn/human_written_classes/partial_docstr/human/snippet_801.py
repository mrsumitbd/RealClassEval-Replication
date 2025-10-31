class NodeIterator:
    """
    The L{Element} child node iterator.
    @ivar pos: The current position
    @type pos: int
    @ivar children: A list of a child nodes.
    @type children: [L{Element},..]
    """

    def __init__(self, parent):
        """
        @param parent: An element to iterate.
        @type parent: L{Element}
        """
        self.pos = 0
        self.children = parent.children

    def __next__(self):
        return self.next()

    def next(self):
        """
        Get the next child.
        @return: The next child.
        @rtype: L{Element}
        @raise StopIterator: At the end.
        """
        try:
            child = self.children[self.pos]
            self.pos += 1
            return child
        except:
            raise StopIteration()