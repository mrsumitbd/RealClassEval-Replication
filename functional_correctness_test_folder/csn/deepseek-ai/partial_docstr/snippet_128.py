
class PartitionRefinement:

    def __init__(self, n):
        self.partition = [set(range(n))]
        self.n = n

    def refine(self, pivot):
        pivot_set = set(pivot)
        new_partition = []
        for C in self.partition:
            intersect = C & pivot_set
            difference = C - pivot_set
            if intersect:
                new_partition.append(intersect)
            if difference:
                new_partition.append(difference)
        self.partition = new_partition

    def tolist(self):
        return [sorted(C) for C in self.partition]

    def order(self):
        order = []
        for C in self.partition:
            order.extend(sorted(C))
        return order
