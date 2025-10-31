class PartitionRefinement:

    def __init__(self, n):
        self.n = int(n)
        if self.n < 0:
            raise ValueError("n must be non-negative")
        self._blocks = [list(range(self.n))] if self.n > 0 else []

    def refine(self, pivot):
        pivot_set = set(pivot)
        if not self._blocks or not pivot_set:
            return
        new_blocks = []
        for block in self._blocks:
            if not block:
                continue
            in_pivot = []
            not_in_pivot = []
            for x in block:
                (in_pivot if x in pivot_set else not_in_pivot).append(x)
            if in_pivot and not_in_pivot:
                new_blocks.append(in_pivot)
                new_blocks.append(not_in_pivot)
            else:
                new_blocks.append(block)
        self._blocks = new_blocks

    def tolist(self):
        return [b[:] for b in self._blocks]

    def order(self):
        return [x for block in self._blocks for x in block]
