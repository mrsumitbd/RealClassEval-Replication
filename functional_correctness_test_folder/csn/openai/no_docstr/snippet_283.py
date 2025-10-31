class ProgressBarStream:
    def __init__(self, stream):
        self.stream = stream

    def write(self, *args, **kwargs):
        return self.stream.write(*args, **kwargs)

    def flush(self):
        return self.stream.flush()
