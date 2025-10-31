
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
        self.element_to_class = {i: 0 for i in range(n)}
        self.class_order = [0]

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        pivot_set = set(pivot)
        new_classes = []
        affected_classes = set()

        for elem in pivot:
            class_idx = self.element_to_class[elem]
            affected_classes.add(class_idx)

        for class_idx in affected_classes:
            original_class = self.partition[class_idx]
            intersection = []
            difference = []

            for elem in original_class:
                if elem in pivot_set:
                    intersection.append(elem)
                else:
                    difference.append(elem)

            if intersection and difference:
                self.partition[class_idx] = intersection
                new_class_idx = len(self.partition)
                self.partition.append(difference)

                for elem in difference:
                    self.element_to_class[elem] = new_class_idx

                new_classes.append(new_class_idx)

        self.class_order = []
        for idx in self.class_order:
            if idx in affected_classes:
                self.class_order.append(idx)
                for new_idx in new_classes:
                    if new_idx not in self.class_order:
                        self.class_order.append(new_idx)
            else:
                self.class_order.append(idx)

        for new_idx in new_classes:
            if new_idx not in self.class_order:
                self.class_order.append(new_idx)

    def tolist(self):
        '''produce a list representation of the partition
        '''
        return [cls for cls in self.partition if cls]

    def order(self):
        '''Produce a flatten list of the partition, ordered by classes
        '''
        ordered = []
        for class_idx in self.class_order:
            if class_idx < len(self.partition):
                ordered.extend(self.partition[class_idx])
        return ordered
