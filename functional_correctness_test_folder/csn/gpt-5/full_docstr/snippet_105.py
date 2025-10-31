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
        if len(buffers) == 1 and hasattr(buffers[0], '__iter__') and not hasattr(buffers[0], '__getitem__'):
            buffers = tuple(buffers[0])
        self._buffers = list(buffers)
        self._cum = []
        total = 0
        for b in self._buffers:
            n = len(b)
            total += n
            self._cum.append(total)
        self._len = total

    def __len__(self):
        '''The number of segments within all ``BufferWithSegments``.'''
        return self._len

    def __getitem__(self, i):
        '''Obtain the ``BufferSegment`` at an offset.'''
        if isinstance(i, slice):
            start, stop, step = i.indices(self._len)
            if step == 1:
                # Fast path: gather contiguous ranges from underlying buffers
                result = []
                if start >= stop:
                    return result
                cur = start
                while cur < stop:
                    # find buffer containing cur
                    buf_idx = self._find_buffer_index(cur)
                    prev_cum = 0 if buf_idx == 0 else self._cum[buf_idx - 1]
                    local_start = cur - prev_cum
                    # maximum local index we can take from this buffer
                    local_end_cap = self._cum[buf_idx] - prev_cum
                    take = min(local_end_cap, local_start + (stop - cur))
                    # extend from local_start to take (exclusive)
                    b = self._buffers[buf_idx]
                    result.extend(b[local_start:take])
                    cur += (take - local_start)
                return result
            else:
                return [self[idx] for idx in range(start, stop, step)]
        # integer index
        idx = i
        if idx < 0:
            idx += self._len
        if idx < 0 or idx >= self._len:
            raise IndexError('index out of range')
        buf_idx = self._find_buffer_index(idx)
        prev_cum = 0 if buf_idx == 0 else self._cum[buf_idx - 1]
        local_idx = idx - prev_cum
        return self._buffers[buf_idx][local_idx]

    def _find_buffer_index(self, global_index):
        # binary search over cumulative counts
        lo, hi = 0, len(self._cum)
        while lo < hi:
            mid = (lo + hi) // 2
            if global_index < self._cum[mid]:
                hi = mid
            else:
                lo = mid + 1
        return lo
