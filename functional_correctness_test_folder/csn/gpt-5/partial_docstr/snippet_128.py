class PartitionRefinement:

    def __init__(self, n):
        self.n = n
        self.elems = list(range(n))          # current order of elements
        # position of each element in elems
        self.pos = list(range(n))
        # start index (inclusive) for each block
        self.block_start = [0]
        # end index (exclusive) for each block
        self.block_end = [n]
        # current split pointer for each block (used during refine)
        self.split = [0]
        # current block index for each element
        self.block_id = [0] * n

    def _swap_positions(self, i, j):
        if i == j:
            return
        a, b = self.elems[i], self.elems[j]
        self.elems[i], self.elems[j] = b, a
        self.pos[a], self.pos[b] = j, i

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        num_blocks = len(self.block_start)
        touched = []
        touched_flag = [False] * num_blocks

        for x in pivot:
            b = self.block_id[x]
            # mark block as touched (once)
            if not touched_flag[b]:
                touched_flag[b] = True
                touched.append(b)
            # pack x into the front segment of its block if not already
            s = self.block_start[b]
            sp = self.split[b]
            i = self.pos[x]
            if i >= sp:  # not yet in the marked prefix
                self._swap_positions(i, sp)
                self.split[b] = sp + 1

        # perform splits on touched blocks
        for b in touched:
            s = self.block_start[b]
            e = self.block_end[b]
            m = self.split[b] - s          # number of marked in block
            size = e - s

            if m == 0 or m == size:
                # no split needed, just reset split pointer
                self.split[b] = s
                continue

            # create a new block for the smaller side to keep work linear
            if m <= size - m:
                # smaller side is the marked prefix [s, s+m)
                new_start, new_end = s, s + m
                # old block becomes unmarked suffix [s+m, e)
                self.block_start[b] = s + m
                # new block appended
                new_b = len(self.block_start)
                self.block_start.append(new_start)
                self.block_end.append(new_end)
                self.split.append(new_start)
                # update end of old block
                self.block_end[b] = e
                # update block_id for elements in new small block
                for idx in range(new_start, new_end):
                    self.block_id[self.elems[idx]] = new_b
                # reset split for old block
                self.split[b] = self.block_start[b]
            else:
                # smaller side is the unmarked suffix [s+m, e)
                new_start, new_end = s + m, e
                # old block becomes marked prefix [s, s+m)
                self.block_end[b] = s + m
                # new block appended
                new_b = len(self.block_start)
                self.block_start.append(new_start)
                self.block_end.append(new_end)
                self.split.append(new_start)
                # update block_id for elements in new small block
                for idx in range(new_start, new_end):
                    self.block_id[self.elems[idx]] = new_b
                # reset split for old block
                self.split[b] = self.block_start[b]

    def tolist(self):
        res = []
        for s, e in zip(self.block_start, self.block_end):
            res.append(self.elems[s:e].copy())
        return res

    def order(self):
        return self.elems.copy()
