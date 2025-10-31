
import sys


class PrintAndFlushSink:
    """
    A simple sink that writes messages to stdout and flushes immediately.
    """

    def write(self, message: str):
        """Write the message to stdout and flush immediately."""
        sys.stdout.write(message)
        sys.stdout.flush()

    def flush(self):
        """
        Flush the stream.
        Already flushed on every write call.
        """
        pass
