
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
        if not buffers:
            raise ValueError(
                "At least one BufferWithSegments instance is required")
        for buf in buffers:
            if not hasattr(buf, "__len__") or not hasattr(buf, "__getitem__"):
                raise TypeError(
                    "All arguments must be BufferWithSegments-like objects")
        self._buffers = buffers
        # Precompute cumulative segment counts for fast indexing
        self._cumulative = []
        total = 0
        for buf in self._buffers:
            total += len(buf)
            self._cumulative.append(total)

    def __len__(self):
        '''The number of segments within all ``BufferWithSegments``.'''
        return self._cumulative[-1] if self._cumulative else 0

    def _find_buffer(self, idx):
        """Return (buffer_index, local_index) for a global index."""
        if idx < 0:
            idx += len(self)
        if idx < 0 or idx >= len(self):
            raise IndexError("segment index out of range")
        # Binary search over cumulative counts
        lo, hi = 0, len(self._cumulative) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if idx < self._cumulative[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        buf_idx = lo
        prev_cum = self._cumulative[buf_idx - 1] if buf_idx > 0 else 0
        local_idx = idx - prev_cum
        return buf_idx, local_idx

    def __getitem__(self, i):
        '''Obtain the ``BufferSegment`` at an offset.'''
        if isinstance(i, slice):
            # Return a list of segments for the slice
            start, stop, step = i.indices(len(self))
            return [self[j] for j in range(start, stop, step)]
        if not isinstance(i, int):
            raise TypeError("indices must be integers or slices")
        buf_idx, local_idx = self._find_buffer(i)
        return self._buffers[buf_idx][local_idx]

    def __iter__(self):
        for buf in self._buffers:
            for seg in buf:
                yield seg

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(repr(b) for b in self._buffers)})"
