
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
        self.buffers = buffers
        self._segment_counts = [len(buffer) for buffer in buffers]
        self._cumulative_counts = []
        total = 0
        for count in self._segment_counts:
            total += count
            self._cumulative_counts.append(total)

    def __len__(self):
        '''The number of segments within all ``BufferWithSegments``.'''
        return sum(self._segment_counts)

    def __getitem__(self, i):
        '''Obtain the ``BufferSegment`` at an offset.'''
        if i < 0 or i >= len(self):
            raise IndexError("Index out of range")

        buffer_idx = 0
        while buffer_idx < len(self._cumulative_counts) and i >= self._cumulative_counts[buffer_idx]:
            buffer_idx += 1

        if buffer_idx == 0:
            segment_idx = i
        else:
            segment_idx = i - self._cumulative_counts[buffer_idx - 1]

        return self.buffers[buffer_idx][segment_idx]
