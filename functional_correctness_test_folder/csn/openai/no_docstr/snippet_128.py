
class PartitionRefinement:
    """
    A simple partition refinement data structure.

    The partition is represented as a list of blocks, each block being a list of elements.
    The initial partition contains a single block with all elements from 0 to n-1.

    Methods
    -------
    refine(pivot)
        Refines the current partition by splitting each block into the intersection
        with the pivot set and the difference. The pivot can be any iterable of
        elements. If an element is not present in the current partition it is ignored.
    tolist()
        Returns a shallow copy of the current partition as a list of lists.
    order()
        Returns a flat list of all elements in the order induced by the partition.
    """

    def __init__(self, n):
        # Start with a single block containing all elements 0..n-1
        self.blocks = [list(range(n))]

    def refine(self, pivot):
        # Convert pivot to a set for O(1) membership tests
        pivot_set = set(pivot)
        new_blocks = []
        for block in self.blocks:
            # Compute intersection and difference
            inter = [x for x in block if x in pivot_set]
            diff = [x for x in block if x not in pivot_set]
            # Replace block with the two parts if both are non-empty
            if inter and diff:
                new_blocks.append(inter)
                new_blocks.append(diff)
            else:
                # Keep the block unchanged if it is not split
                new_blocks.append(block)
        self.blocks = new_blocks

    def tolist(self):
        # Return a shallow copy of the blocks list
        return [list(b) for b in self.blocks]

    def order(self):
        # Flatten the blocks into a single list preserving block order
        return [x for block in self.blocks for x in block]
