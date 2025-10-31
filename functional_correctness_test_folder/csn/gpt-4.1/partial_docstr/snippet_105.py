
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
        self._buffers = list(buffers)
        self._segment_counts = [len(buf) for buf in self._buffers]
        self._cumulative = []
        total = 0
        for count in self._segment_counts:
            self._cumulative.append(total)
            total += count
        self._total_segments = total

    def __len__(self):
        return self._total_segments

    def __getitem__(self, i):
        if isinstance(i, slice):
            # Support slicing
            indices = range(*i.indices(len(self)))
            return [self[j] for j in indices]
        if i < 0:
            i += len(self)
        if not (0 <= i < len(self)):
            raise IndexError("segment index out of range")
        # Find which buffer this index falls into
        # self._cumulative is a list of starting indices for each buffer
        # Use binary search for efficiency
        left, right = 0, len(self._cumulative) - 1
        while left <= right:
            mid = (left + right) // 2
            if self._cumulative[mid] <= i < (self._cumulative[mid] + self._segment_counts[mid]):
                buf_idx = mid
                seg_idx = i - self._cumulative[mid]
                return self._buffers[buf_idx][seg_idx]
            elif i < self._cumulative[mid]:
                right = mid - 1
            else:
                left = mid + 1
        raise IndexError("segment index out of range")
