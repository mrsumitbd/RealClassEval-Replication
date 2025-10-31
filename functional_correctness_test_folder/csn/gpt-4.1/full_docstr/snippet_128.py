
class PartitionRefinement:
    '''This data structure implements an order preserving
    partition with refinements.
    '''

    def __init__(self, n):
        '''Start with the partition consisting of the unique class {0,1,..,n-1}
        complexity: O(n) both in time and space
        '''
        self.n = n
        self.partition = [list(range(n))]
        self.elem_to_class = [0] * n  # maps element to its class index

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        pivot_set = set(pivot)
        new_partition = []
        new_elem_to_class = [None] * self.n

        for cls in self.partition:
            in_pivot = []
            not_in_pivot = []
            for x in cls:
                if x in pivot_set:
                    in_pivot.append(x)
                else:
                    not_in_pivot.append(x)
            if in_pivot:
                new_partition.append(in_pivot)
            if not_in_pivot:
                new_partition.append(not_in_pivot)

        # Update elem_to_class
        idx = 0
        for cls in new_partition:
            for x in cls:
                new_elem_to_class[x] = idx
            idx += 1

        self.partition = new_partition
        self.elem_to_class = new_elem_to_class

    def tolist(self):
        '''produce a list representation of the partition
        '''
        return [cls.copy() for cls in self.partition]

    def order(self):
        '''Produce a flatten list of the partition, ordered by classes
        '''
        return [x for cls in self.partition for x in cls]
