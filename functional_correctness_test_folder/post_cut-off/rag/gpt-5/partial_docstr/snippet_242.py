import sys


class ImmediateFlushSink:
    '''A custom Loguru sink that writes to a stream and flushes immediately after each message.
    This ensures that logs appear in real time.
    '''

    def __init__(self, stream=None):
        '''Initialize the ImmediateFlushSink.
        Args:
            stream (Stream, optional): The stream to write to. Defaults to sys.stderr.
        '''
        self._stream = stream if stream is not None else sys.stderr

    def write(self, message):
        '''Write a message to the stream and flush immediately.
        Args:
            message (str): The message to write.
        '''
        try:
            self._stream.write(str(message))
        except TypeError:
            # Fallback in case the stream expects bytes
            data = str(message).encode(
                getattr(self._stream, "encoding", "utf-8") or "utf-8", errors="replace")
            self._stream.write(data)
        self.flush()

    def flush(self):
        '''Flush the stream.'''
        if hasattr(self._stream, 'flush'):
            self._stream.flush()
