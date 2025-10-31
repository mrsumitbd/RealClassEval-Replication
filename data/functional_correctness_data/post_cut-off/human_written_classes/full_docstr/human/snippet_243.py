class PrintAndFlushSink:
    """A Loguru sink.

    forcibly prints each log record and flushes immediately,
    mimicking print(..., flush=True).
    """

    def write(self, message: str):
        """Write a message to the stream and flush immediately.

        Args:
            message (str): The message to write.
        """
        print(message, end='', flush=True)

    def flush(self):
        """Flush the stream.

        Already flushed on every write call.
        """
        pass