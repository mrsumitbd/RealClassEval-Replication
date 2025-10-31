
class PartitionRefinement:

    def __init__(self, n):
        self.partition = [set([i]) for i in range(n)]
        self.active = set(range(n))

    def refine(self, pivot):
        new_partition = []
        for cell in self.partition:
            split = [set(), set()]
            for element in cell:
                split[pivot[element]].add(element)
            new_partition.extend(split)
        self.partition = [cell for cell in new_partition if cell]
        self.active = set().union(
            *[cell for cell in self.partition if len(cell) > 1])

    def tolist(self):
        return [list(cell) for cell in self.partition]

    def order(self):
        return sorted(self.active)
