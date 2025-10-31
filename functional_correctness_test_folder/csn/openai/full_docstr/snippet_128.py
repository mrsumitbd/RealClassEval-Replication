
class PartitionRefinement:
    '''This data structure implements an order preserving
    partition with refinements.
    '''

    class _Class:
        __slots__ = ("elements",)

        def __init__(self, elements):
            self.elements = elements

    def __init__(self, n):
        '''Start with the partition consisting of the unique class {0,1,..,n-1}
        complexity: O(n) both in time and space
        '''
        self.n = n
        init_class = self._Class(list(range(n)))
        self.classes = [init_class]
        self.element_to_class = [init_class] * n

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        pivot = list(pivot)
        # group pivot elements by their current class
        class_to_pivots = {}
        for e in pivot:
