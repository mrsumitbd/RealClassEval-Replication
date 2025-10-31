class BufferWithSegmentsCollection:
    '''A virtual spanning view over multiple BufferWithSegments.
    Instances are constructed from 1 or more :py:class:`BufferWithSegments`
    instances. The resulting object behaves like an ordered sequence whose
    members are the segments within each ``BufferWithSegments``.
    If the object is composed of 2 ``BufferWithSegments`` instances with the
    first having 2 segments and the second have 3 segments, then ``b[0]``
    and ``b[1]`` access segments in the first object and ``b[2]``, ``b[3]``,
    and ``b[4]`` access segments from the second.
    '''

    def __init__(self, *buffers):
        if len(buffers) == 1 and hasattr(buffers[0], "__iter__") and not hasattr(buffers[0], "read"):
            self._buffers = list(buffers[0])
        else:
            self._buffers = list(buffers)
        self._starts = [0]
        total = 0
        for b in self._buffers:
            total += len(b)
            self._starts.append(total)
        self._total = total

    def __len__(self):
        return self._total

    def __getitem__(self, i):
        if isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            return [self[j] for j in range(start, stop, step)]
        n = len(self)
        if i < 0:
            i += n
        if i < 0 or i >= n:
            raise IndexError("index out of range")
        # binary search over starts
        lo, hi = 0, len(self._starts) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if self._starts[mid + 1] <= i:
                lo = mid + 1
            elif self._starts[mid] > i:
                hi = mid
            else:
                lo = mid
                break
        buf_idx = lo
        local_idx = i - self._starts[buf_idx]
        return self._buffers[buf_idx][local_idx]
