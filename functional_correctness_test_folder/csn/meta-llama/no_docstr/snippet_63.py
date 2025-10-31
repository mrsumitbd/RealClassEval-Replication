
class StreamingFile:

    def __init__(self, data_stream):
        """
        Initialize the StreamingFile object.

        Args:
            data_stream: A generator or iterable that yields chunks of data.
        """
        self.data_stream = iter(data_stream)
        self.buffer = b''

    def read(self, size=None):
        """
        Read data from the stream.

        Args:
            size (int, optional): The number of bytes to read. If None, read until the end of the stream.

        Returns:
            bytes: The data read from the stream.
        """
        if size is None:
            # Read until the end of the stream
            result = self.buffer
            self.buffer = b''
            for chunk in self.data_stream:
                result += chunk
            return result
        else:
            # Read until we have 'size' bytes in the buffer
            while len(self.buffer) < size:
                try:
                    chunk = next(self.data_stream)
                    self.buffer += chunk
                except StopIteration:
                    # We've reached the end of the stream
                    break
            # Return the requested amount of data
            result = self.buffer[:size]
            self.buffer = self.buffer[size:]
            return result

# Example usage:


def data_stream():
    yield b'Hello, '
    yield b'world!'
    yield b' This is a test.'


streaming_file = StreamingFile(data_stream())
print(streaming_file.read(5))  # b'Hello'
print(streaming_file.read())   # b', world! This is a test.'
