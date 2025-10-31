
class ImmediateFlushSink:

    def __init__(self, stream=None):
        self.stream = stream or sys.stdout

    def write(self, message):
        self.stream.write(message)
        self.flush()

    def flush(self):
        self.stream.flush()
