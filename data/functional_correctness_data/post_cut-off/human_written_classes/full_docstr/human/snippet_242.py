import sys

class ImmediateFlushSink:
    """A custom Loguru sink that writes to a stream and flushes immediately after each message.

    This ensures that logs appear in real time.
    """

    def __init__(self, stream=None):
        """Initialize the ImmediateFlushSink.

        Args:
            stream (Stream, optional): The stream to write to. Defaults to sys.stderr.
        """
        self._stream = stream if stream else sys.stderr

    def write(self, message):
        """Write a message to the stream and flush immediately.

        Args:
            message (str): The message to write.
        """
        self._stream.write(message)
        self._stream.flush()

    def flush(self):
        """Flush the stream."""
        self._stream.flush()