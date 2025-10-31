import sys
from typing import Optional


class ImmediateFlushSink:
    '''A custom Loguru sink that writes to a stream and flushes immediately after each message.
    This ensures that logs appear in real time.
    '''

    def __init__(self, stream: Optional[object] = None):
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
            self._stream.write(message if isinstance(
                message, str) else str(message))
        except Exception:
            # Best-effort fallback to avoid crashing on logging
            try:
                self._stream.write(str(message))
            except Exception:
                return
        self.flush()

    def flush(self):
        '''Flush the stream.'''
        try:
            flush = getattr(self._stream, "flush", None)
            if callable(flush):
                flush()
        except Exception:
            # Silently ignore flush errors to avoid breaking logging
            pass
