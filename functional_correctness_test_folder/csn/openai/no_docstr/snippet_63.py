
class StreamingFile:
    def __init__(self, data_stream):
        """
        Initialize the StreamingFile with a data stream.

        Parameters
        ----------
        data_stream : file-like object or iterable
            The underlying data source. It can be a file-like object
            that implements a `read` method, or any iterable that yields
            bytes-like objects (bytes, bytearray, or strings).
        """
        # If the stream has a read method, use it directly.
        if hasattr(data_stream, "read") and callable(data_stream.read):
            self._stream = data_stream
            self._iter = None
        else:
            # Wrap the iterable in an iterator.
            self._stream = None
            self._iter = iter(data_stream)
        self._buffer = bytearray()
        self._exhausted = False

    def _fill_buffer(self, min_bytes=1):
        """
        Fill the internal buffer until it contains at least `min_bytes`
        or until the underlying stream is exhausted.
        """
        if self._exhausted:
            return

        while len(self._buffer) < min_bytes and not self._exhausted:
            try:
                if self._stream is not None:
                    # Read a chunk from the file-like object.
                    chunk = self._stream.read(min_bytes - len(self._buffer))
                    if not chunk:
                        self._exhausted = True
                        break
                    # Ensure we have bytes.
                    if isinstance(chunk, str):
                        chunk = chunk.encode()
                    self._buffer.extend(chunk)
                else:
                    # Read the next item from the iterator.
                    chunk = next(self._iter)
                    if isinstance(chunk, str):
                        chunk = chunk.encode()
                    elif isinstance(chunk, (bytes, bytearray)):
                        pass
                    else:
                        # Try to convert to bytes.
                        chunk = bytes(chunk)
                    self._buffer.extend(chunk)
            except StopIteration:
                self._exhausted = True
                break

    def read(self, size=None):
        """
        Read up to `size` bytes from the stream.

        Parameters
        ----------
        size : int or None, optional
            Number of bytes to read. If None, read all remaining data.

        Returns
        -------
        bytes
            The data read from the stream.
        """
        if size is None:
            # Read everything.
            self._fill_buffer()
            data = bytes(self._buffer)
            self._buffer.clear()
            return data

        if size <= 0:
            return b""

        # Ensure we have enough data in the buffer.
        self._fill_buffer(min_bytes=size)

        # Slice the required amount.
        data = self._buffer[:size]
        # Remove the consumed bytes from the buffer.
        del self._buffer[:size]
        return bytes(data)
