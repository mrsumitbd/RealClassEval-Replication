class ImmediateFlushSink:

    def __init__(self, stream=None):
        import sys
        self.stream = stream if stream is not None else sys.stdout
        if not hasattr(self.stream, 'write') or not hasattr(self.stream, 'flush'):
            raise ValueError(
                "Provided stream must have 'write' and 'flush' methods.")

    def write(self, message):
        if message is None:
            message = ""
        written = self.stream.write(str(message))
        self.stream.flush()
        return written

    def flush(self):
        '''Flush the stream.'''
        self.stream.flush()
