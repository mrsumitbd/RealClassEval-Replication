
class BufferSegment:
    def __init__(self, data, offset=0):
        """
        Initialize a BufferSegment instance.

        Args:
            data (bytes or BufferSegment): The data to be stored in the segment.
            offset (int, optional): The offset of the segment. Defaults to 0.
        """
        if isinstance(data, BufferSegment):
            self._data = data._data
            self._offset = data._offset + offset
        else:
            self._data = data
            self._offset = offset

    @property
    def offset(self):
        """
        Get the offset of the segment.

        Returns:
            int: The offset of the segment.
        """
        return self._offset

    def __len__(self):
        """
        Get the length of the segment.

        Returns:
            int: The length of the segment.
        """
        return len(self._data)

    def tobytes(self):
        """
        Convert the segment to bytes.

        Returns:
            bytes: The bytes representation of the segment.
        """
        return self._data
