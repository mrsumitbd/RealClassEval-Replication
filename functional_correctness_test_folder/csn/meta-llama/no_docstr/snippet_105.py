
class BufferWithSegmentsCollection:
    def __init__(self, buffer, segments):
        """
        Initialize the BufferWithSegmentsCollection.

        Args:
        buffer (bytes or bytearray): The underlying buffer.
        segments (list of tuples): A list of tuples where each tuple contains 
            the start and end indices of a segment in the buffer.
        """
        self.buffer = buffer
        self.segments = segments

    def __len__(self):
        """
        Return the number of segments in the collection.

        Returns:
        int: The number of segments.
        """
        return len(self.segments)

    def __getitem__(self, i):
        """
        Return the segment at the specified index.

        Args:
        i (int or slice): The index or slice of the segment(s) to retrieve.

        Returns:
        bytes or list of bytes: The segment(s) at the specified index or slice.
        """
        if isinstance(i, int):
            if i < 0:
                i += len(self)
            if i < 0 or i >= len(self):
                raise IndexError("Index out of range")
            start, end = self.segments[i]
            return self.buffer[start:end]
        elif isinstance(i, slice):
            return [self.buffer[start:end] for start, end in self.segments[i]]
        else:
            raise TypeError("Index must be an integer or slice")


# Example usage:
if __name__ == "__main__":
    buffer = b"Hello, World!"
    segments = [(0, 5), (7, 12)]
    collection = BufferWithSegmentsCollection(buffer, segments)
    print(len(collection))  # Output: 2
    print(collection[0])    # Output: b'Hello'
    print(collection[1])    # Output: b'World'
    print(collection[:])    # Output: [b'Hello', b'World']
