
class BufferWithSegmentsCollection:
    def __init__(self, buffer: bytes, segment_size: int):
        if segment_size <= 0:
            raise ValueError("segment_size must be a positive integer")
        self._segments = [
            buffer[i:i + segment_size] for i in range(0, len(buffer), segment_size)
        ]

    def __len__(self):
        return len(self._segments)

    def __getitem__(self, i):
        return self._segments[i]
