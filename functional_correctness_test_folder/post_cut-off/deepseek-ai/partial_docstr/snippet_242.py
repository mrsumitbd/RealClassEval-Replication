
class ImmediateFlushSink:

    def __init__(self, stream=None):
        self.stream = stream

    def write(self, message):
        if self.stream is not None:
            self.stream.write(message)
            self.flush()

    def flush(self):
        '''Flush the stream.'''
        if self.stream is not None:
            self.stream.flush()
