class DoublyLinkedListIterator:

    def __init__(self, node, reverse=False):
        self.node = ListNode(None, node, node)
        self.reverse = reverse

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.reverse:
            if self.node.prev is not None:
                self.node = self.node.prev
                return self.node
        elif self.node.next is not None:
            self.node = self.node.next
            return self.node
        raise StopIteration()

    def __reversed__(self):
        return DoublyLinkedListIterator(self.node, not self.reverse)