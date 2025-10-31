
class ProgressBarStream:

    def __init__(self, stream):
        self.stream = stream

    def write(self, *args, **kwargs):
        self.stream.write(*args, **kwargs)

    def flush(self):
        self.stream.flush()
