
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
        self.lengths = [len(buffer) for buffer in buffers]
        self.total_length = sum(self.lengths)

    def __len__(self):
        return self.total_length

    def __getitem__(self, i):
        if isinstance(i, int):
            if i < 0:
                i += self.total_length
            if i < 0 or i >= self.total_length:
                raise IndexError('Index out of range')
            buffer_index = 0
            while i >= self.lengths[buffer_index]:
                i -= self.lengths[buffer_index]
                buffer_index += 1
            return self.buffers[buffer_index][i]
        elif isinstance(i, slice):
            start, stop, step = i.indices(self.total_length)
            result = []
            buffer_index = 0
            current_index = 0
            while current_index < stop:
                if current_index >= start and (current_index - start) % step == 0:
                    result.append(
                        self.buffers[buffer_index][current_index - sum(self.lengths[:buffer_index])])
                if current_index >= sum(self.lengths[:buffer_index + 1]):
                    buffer_index += 1
                current_index += 1
            return result
        else:
            raise TypeError('Index must be an integer or slice')
