
class PartitionRefinement:

    def __init__(self, n):
        self.n = n
        self._blocks = [list(range(n))]
        self._elem_to_block = [0] * n

    def refine(self, pivot):
        # pivot: iterable of elements to split on
        pivot_set = set(pivot)
        new_blocks = []
        new_elem_to_block = self._elem_to_block[:]
        for block_idx, block in enumerate(self._blocks):
            in_pivot = []
            not_in_pivot = []
            for x in block:
                if x in pivot_set:
                    in_pivot.append(x)
                else:
                    not_in_pivot.append(x)
            if in_pivot and not_in_pivot:
                # split block
                new_blocks.append(not_in_pivot)
                for x in not_in_pivot:
                    new_elem_to_block[x] = len(new_blocks) - 1
                new_blocks.append(in_pivot)
                for x in in_pivot:
                    new_elem_to_block[x] = len(new_blocks) - 1
            else:
                new_blocks.append(block)
                for x in block:
                    new_elem_to_block[x] = len(new_blocks) - 1
        self._blocks = [b for b in new_blocks if b]
        # Recompute mapping
        self._elem_to_block = [0] * self.n
        for i, block in enumerate(self._blocks):
            for x in block:
                self._elem_to_block[x] = i

    def tolist(self):
        return [block[:] for block in self._blocks]

    def order(self):
        res = []
        for block in self._blocks:
            res.extend(block)
        return res
