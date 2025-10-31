
class PartitionRefinement:
    '''This data structure implements an order preserving
    partition with refinements.
    '''

    def __init__(self, n):
        '''Start with the partition consisting of the unique class {0,1,..,n-1}
        complexity: O(n) both in time and space
        '''
        self.partition = [set(range(n))]
        self.element_to_class = {i: 0 for i in range(n)}

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        new_partition = []
        new_element_to_class = {}
        for i, cls in enumerate(self.partition):
            intersection = cls & pivot
            setminus = cls - pivot
            if intersection:
                new_partition.append(intersection)
                for elem in intersection:
                    new_element_to_class[elem] = len(new_partition) - 1
            if setminus:
                new_partition.append(setminus)
                for elem in setminus:
                    new_element_to_class[elem] = len(new_partition) - 1
        self.partition = new_partition
        self.element_to_class = new_element_to_class

    def tolist(self):
        '''produce a list representation of the partition
        '''
        return [list(cls) for cls in self.partition]

    def order(self):
        '''Produce a flatten list of the partition, ordered by classes
        '''
        ordered_list = []
        for cls in self.partition:
            ordered_list.extend(cls)
        return ordered_list
