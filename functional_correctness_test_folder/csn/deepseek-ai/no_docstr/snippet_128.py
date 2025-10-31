
class PartitionRefinement:

    def __init__(self, n):
        self.partitions = [set(range(n))]
        self.n = n

    def refine(self, pivot):
        new_partitions = []
        for part in self.partitions:
            intersection = part & pivot
            difference = part - pivot
            if intersection:
                new_partitions.append(intersection)
            if difference:
                new_partitions.append(difference)
        self.partitions = new_partitions

    def tolist(self):
        return [sorted(part) for part in self.partitions]

    def order(self):
        order = []
        for part in self.partitions:
            order.extend(sorted(part))
        return order
