class DoubleLinkedListItem:
    """Item of a circular double linked list
    """

    def __init__(self, anchor=None):
        """Create a new item to be inserted before item anchor.
           if anchor is None: create a single item circular double linked list
        """
        if anchor:
            self.insert(anchor)
        else:
            self.prec = self
            self.succ = self

    def remove(self):
        self.prec.succ = self.succ
        self.succ.prec = self.prec

    def insert(self, anchor):
        """insert list item before anchor
        """
        self.prec = anchor.prec
        self.succ = anchor
        self.succ.prec = self
        self.prec.succ = self

    def __iter__(self):
        """iterate trough circular list.
        warning: might end stuck in an infinite loop if chaining is not valid
        """
        curr = self
        yield self
        while curr.succ != self:
            curr = curr.succ
            yield curr