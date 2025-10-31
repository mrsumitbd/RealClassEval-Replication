
class ProgressBarStream:

    def __init__(self, stream):
        self.stream = stream

    def write(self, *args, **kwargs):
        if len(args) > 0:
            data = args[0]
            if '\r' in data:
                self.stream.write(data)
                self.stream.flush()
            else:
                self.stream.write(data)

    def flush(self):
        self.stream.flush()
