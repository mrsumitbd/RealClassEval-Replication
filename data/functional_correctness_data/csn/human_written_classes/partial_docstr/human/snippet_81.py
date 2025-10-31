import io

class TqdmBufferedReader(io.BufferedReader):

    def __init__(self, raw, progress_bar):
        """Initializes a new instance of the TqdmBufferedReader class.

        This is a helper class to implement an io.BufferedReader.

        Args:
            raw: The raw bytes data to pass to the buffered reader.
            progress_bar: The progress bar to initialize the reader.
        """
        io.BufferedReader.__init__(self, raw)
        self.progress_bar = progress_bar

    def read(self, *args, **kwargs):
        """Read the buffer, passing named and non named arguments to the io.BufferedReader function."""
        buf = io.BufferedReader.read(self, *args, **kwargs)
        self.increment(len(buf))
        return buf

    def increment(self, length):
        """Increments the reader by a given length.

        Args:
            length: The number of bytes by which to increment the reader.
        """
        self.progress_bar.update(length)