class PartitionRefinement:
    def __init__(self, n):
        # Initially one class containing all elements 0..n-1
        self.partition = [list(range(n))]
        self.elem_to_class = {i: 0 for i in range(n)}

    def refine(self, pivot):
        """Split every class C in the partition into C∩pivot and C\\pivot.
        Complexity is linear in the size of pivot.
        """
        pivot = list(pivot)
        if not pivot:
            return

        # Group pivot elements by the class they belong to
        class_to_pivots = {}
        for e in pivot:
            c = self.elem_to_class[e]
            class_to_pivots.setdefault(c, []).append(e)

        # For each class that intersects pivot, perform the split
        for c, pivots in class_to_pivots.items():
            if len(piv
