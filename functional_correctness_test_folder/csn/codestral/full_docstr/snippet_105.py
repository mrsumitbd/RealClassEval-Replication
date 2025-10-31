
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
        self._segment_offsets = self._calculate_segment_offsets()

    def _calculate_segment_offsets(self):
        offsets = [0]
        for buffer in self.buffers:
            offsets.append(offsets[-1] + len(buffer))
        return offsets

    def __len__(self):
        '''The number of segments within all ``BufferWithSegments``.'''
        return self._segment_offsets[-1]

    def __getitem__(self, i):
        '''Obtain the ``BufferSegment`` at an offset.'''
        if i < 0 or i >= len(self):
            raise IndexError("Index out of range")

        for buffer_idx in range(len(self.buffers)):
            if i < self._segment_offsets[buffer_idx + 1]:
                segment_idx = i - self._segment_offsets[buffer_idx]
                return self.buffers[buffer_idx][segment_idx]

        raise IndexError("Index out of range")
