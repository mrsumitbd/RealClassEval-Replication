class PartitionRefinement:
    '''This data structure implements an order preserving
    partition with refinements.
    '''

    class _Block:
        __slots__ = ("start", "size")

        def __init__(self, start, size):
            self.start = start
            self.size = size

    def __init__(self, n):
        '''Start with the partition consisting of the unique class {0,1,..,n-1}
        complexity: O(n) both in time and space
        '''
        self.n = int(n)
        self.elts = list(range(self.n))
        self.pos = list(range(self.n))
        self.blocks = []
        self.whereblock = [None] * self.n
        b = PartitionRefinement._Block(0, self.n)
        self.blocks.append(b)
        for x in self.elts:
            self.whereblock[x] = b

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        # normalize pivot to unique, valid elements
        piv = set(pivot)
        if not piv:
            return

        # Count marked elements per block and move them to the front of their block
        counts = {}
        touched = set()

        for x in piv:
            if not (0 <= x < self.n):
                continue
            blk = self.whereblock[x]
            # initialize count lazily
            c = counts.get(blk, 0)
            i = self.pos[x]
            j = blk.start + c
            if i != j:
                y = self.elts[j]
                # swap positions i and j
                self.elts[i], self.elts[j] = self.elts[j], self.elts[i]
                self.pos[x], self.pos[y] = j, i
            else:
                self.pos[x] = j  # already true, but keep consistent
            counts[blk] = c + 1
            touched.add(blk)

        if not touched:
            return

        # Perform splits on touched blocks where needed
        for blk in list(touched):
            m = counts.get(blk, 0)
            if m == 0 or m == blk.size:
                continue  # no split needed

            start = blk.start
            size = blk.size

            # Marked part: [start, start+m)
            # Unmarked part: [start+m, start+size)
            idx = self.blocks.index(blk)

            if m <= size - m:
                # Create new block for smaller (marked) part placed before unmarked,
                # keep old block as unmarked (second part)
                new_blk = PartitionRefinement._Block(start, m)
                # Update old block to represent unmarked part
                blk.start = start + m
                blk.size = size - m
                # Insert new block before old block
                self.blocks.insert(idx, new_blk)
                # Update whereblock for elements in new block range
                end = start + m
                for k in range(start, end):
                    self.whereblock[self.elts[k]] = new_blk
            else:
                # Keep old block as marked (first part), create new block for smaller unmarked part
                new_blk = PartitionRefinement._Block(start + m, size - m)
                # Update old block to represent marked part
                blk.start = start
                blk.size = m
                # Insert new block after old block
                self.blocks.insert(idx + 1, new_blk)
                # Update whereblock for elements in new block range
                s2 = start + m
                e2 = start + size
                for k in range(s2, e2):
                    self.whereblock[self.elts[k]] = new_blk

    def tolist(self):
        '''produce a list representation of the partition
        '''
        res = []
        for blk in self.blocks:
            if blk.size > 0:
                res.append(self.elts[blk.start:blk.start + blk.size])
        return res

    def order(self):
        '''Produce a flatten list of the partition, ordered by classes
        '''
        return list(self.elts)
