
class ImmediateFlushSink:

    def __init__(self, stream=None):
        if stream is None:
            import sys
            self.stream = sys.stdout
        else:
            self.stream = stream

    def write(self, message):
        self.stream.write(message)
        self.flush()

    def flush(self):
        self.stream.flush()
