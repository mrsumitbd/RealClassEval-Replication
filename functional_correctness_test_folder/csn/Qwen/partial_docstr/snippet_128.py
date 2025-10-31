
class PartitionRefinement:

    def __init__(self, n):
        self.partition = [{i} for i in range(n)]

    def refine(self, pivot):
        new_partition = []
        for part in self.partition:
            intersection = part.intersection(pivot)
            difference = part.difference(pivot)
            if intersection:
                new_partition.append(intersection)
            if difference:
                new_partition.append(difference)
        self.partition = new_partition

    def tolist(self):
        return [list(part) for part in self.partition]

    def order(self):
        return len(self.partition)
