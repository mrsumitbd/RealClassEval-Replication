
class ProgressBarStream:

    def __init__(self, stream):
        self.stream = stream
        self.progress_bar = None

    def write(self, *args, **kwargs):
        if self.progress_bar is not None:
            self.progress_bar.close()
            self.progress_bar = None
        self.stream.write(*args, **kwargs)

    def flush(self):
        self.stream.flush()
