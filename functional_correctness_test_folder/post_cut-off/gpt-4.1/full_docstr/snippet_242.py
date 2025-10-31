
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
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    def write(self, message):
        '''Write a message to the stream and flush immediately.
        Args:
            message (str): The message to write.
        '''
        self.stream.write(message)
        self.stream.flush()

    def flush(self):
        '''Flush the stream.'''
        self.stream.flush()
