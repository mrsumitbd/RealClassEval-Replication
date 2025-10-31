
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
                "At least one BufferWithSegments instance required")
        self._buffers = tuple(buffers)
        # Precompute cumulative segment counts for fast lookup
        self._cum_counts = []
        total = 0
        for buf in self._buffers:
            total += len(buf)
            self._cum_counts.append(total)

    def __len__(self):
        return self._cum_counts[-1]

    def __getitem__(self, i):
        # Handle slice
        if isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            return [self[j] for j in range(start, stop, step)]

        # Handle integer index
        if not isinstance(i, int):
            raise TypeError(
                f"Index must be int or slice, not {type(i).__name__}")

        n = len(self)
        if i < 0:
            i += n
        if i < 0 or i >= n:
            raise IndexError("Index out of range")

        # Binary search to find the buffer containing the index
        lo, hi = 0, len(self._cum_counts) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if i < self._cum_counts[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        buf_index = lo
        # Compute local index within the buffer
        prev_cum = self._cum_counts[buf_index - 1] if buf_index > 0 else 0
        local_index = i - prev_cum
        return self._buffers[buf_index][local_index]

    def __iter__(self):
        for buf in self._buffers:
            for seg in buf:
                yield seg
