
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
        self._buffers = buffers
        self._lengths = [len(buffer) for buffer in buffers]
        self._cumulative_lengths = [0] * (len(buffers) + 1)
        for i in range(len(buffers)):
            self._cumulative_lengths[i +
                                     1] = self._cumulative_lengths[i] + self._lengths[i]

    def __len__(self):
        '''The number of segments within all ``BufferWithSegments``.'''
        return self._cumulative_lengths[-1]

    def __getitem__(self, i):
        '''Obtain the ``BufferSegment`` at an offset.'''
        if isinstance(i, int):
            if i < 0:
                i += len(self)
            if i < 0 or i >= len(self):
                raise IndexError('Index out of range')
            buffer_index = next(j for j, cumulative_length in enumerate(
                self._cumulative_lengths[1:], start=1) if cumulative_length > i)
            return self._buffers[buffer_index - 1][i - self._cumulative_lengths[buffer_index - 1]]
        elif isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            result = []
            for j in range(start, stop, step):
                result.append(self[j])
            return result
        else:
            raise TypeError('Index must be an integer or slice')
