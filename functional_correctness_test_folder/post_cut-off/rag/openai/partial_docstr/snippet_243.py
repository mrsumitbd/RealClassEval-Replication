
class PrintAndFlushSink:
    '''A Loguru sink.
    forcibly prints each log record and flushes immediately,
    mimicking print(..., flush=True).
    '''

    def write(self, message: str):
        '''Write a message to the stream and flush immediately.
        Args:
            message (str): The message to write.
        '''
        # Loguru may pass messages that already contain a newline.
        # Using print with end='' ensures we don't add an extra newline.
        print(message, end='', flush=True)

    def flush(self):
        '''Flush the stream.
        Already flushed on every write call.
        '''
        # No-op: flushing is handled in write().
        pass
