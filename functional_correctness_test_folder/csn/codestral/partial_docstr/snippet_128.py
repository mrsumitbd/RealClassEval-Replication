
class PartitionRefinement:

    def __init__(self, n):
        self.partition = [set(range(n))]
        self.order_list = list(range(n))

    def refine(self, pivot):
        new_partition = []
        for C in self.partition:
            intersection = C & pivot
            setminus = C - pivot
            if intersection:
                new_partition.append(intersection)
            if setminus:
                new_partition.append(setminus)
        self.partition = new_partition

    def tolist(self):
        return [list(C) for C in self.partition]

    def order(self):
        return self.order_list
