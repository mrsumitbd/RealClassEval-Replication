class BufferWithSegmentsCollection:
    def __len__(self):
        return len(self.segments)

    def __getitem__(self, i):
        n = len(self)
        if isinstance(i, slice):
            start, stop, step = i.indices(n)
            return [self[j] for j in range(start, stop, step)]

        if not isinstance(i, int):
            raise TypeError("Index must be int or slice")

        if i < 0:
            i += n
        if i < 0 or i >= n:
            raise IndexError("Index out of range")

        seg = self.segments[i]

        # Normalize segment to a slice
        if isinstance(seg, slice):
            s = seg
        elif isinstance(seg, tuple) and len(seg) == 2:
            s = slice(seg[0], seg[1])
        elif hasattr(seg, "start") and hasattr(seg, "stop"):
            s = slice(getattr(seg, "start"), getattr(
                seg, "stop"), getattr(seg, "step", None))
        else:
            raise TypeError("Unsupported segment type")

        return self.buffer[s]
