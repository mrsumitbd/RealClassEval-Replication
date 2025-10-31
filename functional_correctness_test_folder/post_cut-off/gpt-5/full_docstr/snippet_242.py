class ImmediateFlushSink:
    '''A custom Loguru sink that writes to a stream and flushes immediately after each message.
    This ensures that logs appear in real time.
    '''

    def __init__(self, stream=None):
        '''Initialize the ImmediateFlushSink.
        Args:
            stream (Stream, optional): The stream to write to. Defaults to sys.stderr.
        '''
        import sys
        self._stream = stream if stream is not None else sys.stderr
        if not hasattr(self._stream, "write"):
            raise ValueError("Provided stream does not have a write() method.")

    def write(self, message):
        '''Write a message to the stream and flush immediately.
        Args:
            message (str): The message to write.
        '''
        if not isinstance(message, (str, bytes)):
            message = str(message)
        if isinstance(message, bytes):
            try:
                message = message.decode("utf-8", errors="replace")
            except Exception:
                message = message.decode(errors="replace")
        self._stream.write(message)
        self.flush()

    def flush(self):
        '''Flush the stream.'''
        if hasattr(self._stream, "flush"):
            self._stream.flush()
