
class PartitionRefinement:
    '''This data structure implements an order preserving
    partition with refinements.
    '''

    def __init__(self, n):
        '''Start with the partition consisting of the unique class {0,1,..,n-1}
        complexity: O(n) both in time and space
        '''
        self.partition = [{i} for i in range(n)]
        self.element_to_class = {i: i for i in range(n)}

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        new_partition = []
        new_element_to_class = self.element_to_class.copy()
        pivot_set = set(pivot)

        for class_index, class_set in enumerate(self.partition):
            intersection = class_set & pivot_set
            difference = class_set - pivot_set

            if intersection:
                new_partition.append(intersection)
                for element in intersection:
                    new_element_to_class[element] = len(new_partition) - 1

            if difference:
                new_partition.append(difference)
                for element in difference:
                    new_element_to_class[element] = len(new_partition) - 1

        self.partition = new_partition
        self.element_to_class = new_element_to_class

    def tolist(self):
        '''produce a list representation of the partition
        '''
        return [list(part) for part in self.partition]

    def order(self):
        '''Produce a flatten list of the partition, ordered by classes
        '''
        return [element for part in self.partition for element in part]
