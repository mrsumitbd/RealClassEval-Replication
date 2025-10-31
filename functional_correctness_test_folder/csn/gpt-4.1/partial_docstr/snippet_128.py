
class PartitionRefinement:
    def __init__(self, n):
        self.n = n
        self.partition = [set(range(n))]

    def refine(self, pivot):
        pivot = set(pivot)
        new_partition = []
        for block in self.partition:
            inter = block & pivot
            diff = block - pivot
            if inter and diff:
                new_partition.append(inter)
                new_partition.append(diff)
            else:
                new_partition.append(block)
        self.partition = new_partition

    def tolist(self):
        return [sorted(list(block)) for block in self.partition]

    def order(self):
        return [i for block in self.partition for i in sorted(block)]
