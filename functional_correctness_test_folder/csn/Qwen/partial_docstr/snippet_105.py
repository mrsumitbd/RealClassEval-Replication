
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
        self._length = sum(len(buf) for buf in buffers)

    def __len__(self):
        return self._length

    def __getitem__(self, i):
        if i < 0 or i >= self._length:
            raise IndexError("Index out of range")

        current_index = 0
        for buf in self.buffers:
            if i < current_index + len(buf):
                return buf[i - current_index]
            current_index += len(buf)

        raise IndexError("Index out of range")
