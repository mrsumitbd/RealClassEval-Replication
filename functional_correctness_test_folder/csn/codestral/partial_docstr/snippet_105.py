
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
        self.segment_indices = []
        for buffer in buffers:
            self.segment_indices.append(len(buffer))

    def __len__(self):
        return sum(self.segment_indices)

    def __getitem__(self, i):
        if i < 0 or i >= len(self):
            raise IndexError("Index out of range")
        buffer_index = 0
        while i >= self.segment_indices[buffer_index]:
            i -= self.segment_indices[buffer_index]
            buffer_index += 1
        return self.buffers[buffer_index][i]
