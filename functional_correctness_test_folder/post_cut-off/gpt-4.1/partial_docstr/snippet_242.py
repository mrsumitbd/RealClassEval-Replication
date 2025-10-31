
class ImmediateFlushSink:

    def __init__(self, stream=None):
        import sys
        self.stream = stream if stream is not None else sys.stdout

    def write(self, message):
        self.stream.write(message)
        self.stream.flush()

    def flush(self):
        '''Flush the stream.'''
        self.stream.flush()
