
class ProgressBarStream:

    def __init__(self, stream):
        self.stream = stream
        self.buffer = ""

    def write(self, *args, **kwargs):
        if args:
            self.buffer += args[0]
            if '\n' in args[0] or '\r' in args[0]:
                self.flush()

    def flush(self):
        self.stream.write(self.buffer)
        self.stream.flush()
        self.buffer = ""
