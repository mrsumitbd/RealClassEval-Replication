
import sys


class ImmediateFlushSink:

    def __init__(self, stream=None):
        self.stream = stream if stream is not None else sys.stdout

    def write(self, message):
        self.stream.write(message)
        self.flush()

    def flush(self):
        self.stream.flush()
