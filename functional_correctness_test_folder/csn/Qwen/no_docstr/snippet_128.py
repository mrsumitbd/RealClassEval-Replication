
class PartitionRefinement:

    def __init__(self, n):
        self.partition = [{i} for i in range(n)]
        self.n = n

    def refine(self, pivot):
        new_partition = []
        for block in self.partition:
            if pivot in block:
                new_block_with_pivot = {pivot}
                new_block_without_pivot = block - new_block_with_pivot
                if new_block_with_pivot:
                    new_partition.append(new_block_with_pivot)
                if new_block_without_pivot:
                    new_partition.append(new_block_without_pivot)
            else:
                new_partition.append(block)
        self.partition = new_partition

    def tolist(self):
        return [list(block) for block in self.partition]

    def order(self):
        return len(self.partition)
