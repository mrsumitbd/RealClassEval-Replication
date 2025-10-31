
class PartitionRefinement:

    def __init__(self, n):
        self.partition = [{i} for i in range(n)]
        self.class_map = {i: i for i in range(n)}

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        new_classes = {}
        for i in pivot:
            class_index = self.class_map[i]
            if class_index not in new_classes:
                new_classes[class_index] = [set(), set()]
            new_classes[class_index][0].add(i)

        for class_index, (in_set, out_set) in new_classes.items():
            out_set.update(self.partition[class_index].difference(in_set))
            if out_set:
                new_class_index = len(self.partition)
                self.partition.append(out_set)
                for i in out_set:
                    self.class_map[i] = new_class_index
                self.partition[class_index] = in_set

    def tolist(self):
        return [list(c) for c in self.partition]

    def order(self):
        return [x for c in self.partition for x in c]
