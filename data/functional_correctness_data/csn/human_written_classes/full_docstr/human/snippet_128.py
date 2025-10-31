class PartitionRefinement:
    """This data structure implements an order preserving
    partition with refinements.
    """

    def __init__(self, n):
        """Start with the partition consisting of the unique class {0,1,..,n-1}
        complexity: O(n) both in time and space
        """
        c = PartitionClass()
        self.classes = c
        self.items = [PartitionItem(i, c) for i in range(n)]

    def refine(self, pivot):
        """Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        """
        has_split = []
        for i in pivot:
            if 0 <= i < len(self.items):
                x = self.items[i]
                c = x.theclass
                if not c.split:
                    c.split = PartitionClass(c)
                    if self.classes is c:
                        self.classes = c.split
                    has_split.append(c)
                x.remove()
                x.theclass = c.split
                c.split.append(x)
        for c in has_split:
            c.split = None
            if not c.items:
                c.remove()
                del c

    def tolist(self):
        """produce a list representation of the partition
        """
        return [[x.val for x in theclass.items] for theclass in self.classes]

    def order(self):
        """Produce a flatten list of the partition, ordered by classes
        """
        return [x.val for theclass in self.classes for x in theclass.items]